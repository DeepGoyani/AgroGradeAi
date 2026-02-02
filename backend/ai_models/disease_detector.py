"""
AgroGrade AI - Dynamic Disease Diagnosis Engine
CONTEXT-AWARE: Only detects diseases VALID for the detected crop
REAL severity calculation via OpenCV lesion segmentation (not fake numbers)
"""

import os
import io
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image

# TensorFlow import
import tensorflow as tf

# =============================================================================
# CONFIGURATION
# =============================================================================
AI_MODELS_DIR = Path(__file__).parent
MODEL_WEIGHTS_DIR = AI_MODELS_DIR / "model_weights"
REMEDY_DB_PATH = AI_MODELS_DIR / "remedy_database.json"

# Create directories
MODEL_WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

# Load remedy database ONCE at startup
def _load_remedy_db() -> Dict:
    if REMEDY_DB_PATH.exists():
        with open(REMEDY_DB_PATH, 'r') as f:
            return json.load(f)
    return {}

REMEDY_DB = _load_remedy_db()

# Disease-specific HSV ranges for lesion detection
DISEASE_COLOR_PROFILES = {
    # Mildew diseases (white/gray patches)
    "powdery_mildew": {"lower": [0, 0, 180], "upper": [180, 30, 255], "type": "light"},
    "grey_mildew": {"lower": [0, 0, 120], "upper": [180, 40, 200], "type": "gray"},
    
    # Blight diseases (brown/black spots)
    "early_blight": {"lower": [10, 50, 20], "upper": [25, 255, 150], "type": "brown"},
    "late_blight": {"lower": [0, 0, 0], "upper": [180, 255, 60], "type": "dark"},
    "bacterial_blight": {"lower": [15, 50, 50], "upper": [30, 255, 180], "type": "brown"},
    
    # Rust diseases (orange/reddish pustules)
    "rust": {"lower": [5, 100, 100], "upper": [20, 255, 255], "type": "orange"},
    
    # Mosaic/Curl diseases (yellowing patterns)
    "leaf_curl": {"lower": [20, 50, 100], "upper": [35, 255, 255], "type": "yellow"},
    "yellow_vein_mosaic": {"lower": [25, 80, 120], "upper": [40, 255, 255], "type": "yellow"},
    "mosaic_virus": {"lower": [20, 40, 100], "upper": [40, 200, 255], "type": "mottled"},
    
    # Spot diseases
    "brown_spot": {"lower": [10, 60, 30], "upper": [25, 255, 150], "type": "brown"},
    "septoria_leaf_spot": {"lower": [0, 0, 100], "upper": [180, 50, 180], "type": "gray_center"},
    "cercospora_leaf_spot": {"lower": [10, 40, 40], "upper": [25, 200, 150], "type": "brown"},
    "purple_blotch": {"lower": [130, 50, 50], "upper": [160, 255, 200], "type": "purple"},
    
    # Other
    "anthracnose": {"lower": [0, 0, 0], "upper": [180, 255, 80], "type": "dark_sunken"},
    "blast": {"lower": [0, 0, 60], "upper": [180, 80, 180], "type": "gray_diamond"},
    "sheath_blight": {"lower": [10, 30, 80], "upper": [30, 150, 200], "type": "tan"},
    
    # Default for unknown diseases
    "default": {"lower": [0, 0, 0], "upper": [180, 255, 100], "type": "generic_dark"}
}


# =============================================================================
# DISEASE DETECTOR CLASS
# =============================================================================
class DiseaseDetector:
    """
    Context-aware disease diagnosis engine.
    
    Features:
    - Only checks diseases VALID for detected crop
    - REAL severity via OpenCV lesion segmentation
    - Dynamic remedies based on crop+disease+severity
    """
    
    def __init__(self, use_pretrained_fallback: bool = True):
        self.disease_models: Dict[str, tf.keras.Model] = {}
        self.disease_labels: Dict[str, List[str]] = {}
        self.use_pretrained_fallback = use_pretrained_fallback
        self.model_version = "v1.0.0"
        
        # Load crop-specific disease models
        self._load_disease_models()
    
    def _load_disease_models(self):
        """Load crop-specific disease classification models"""
        from ai_models.crop_detector import CROP_DISEASES, CROP_LABELS
        
        crops = list(CROP_LABELS.values())
        
        for crop in crops:
            model_path = MODEL_WEIGHTS_DIR / f"{crop}_disease_model.h5"
            labels_path = AI_MODELS_DIR / f"{crop}_disease_labels.json"
            
            # Load model if exists
            if model_path.exists():
                try:
                    self.disease_models[crop] = tf.keras.models.load_model(str(model_path))
                    print(f"✅ Loaded disease model for: {crop}")
                except Exception as e:
                    print(f"⚠️ Failed to load {crop} model: {e}")
            
            # Load or create labels
            if labels_path.exists():
                with open(labels_path, 'r') as f:
                    self.disease_labels[crop] = json.load(f)
            else:
                # Use diseases from crop_diseases.json
                self.disease_labels[crop] = CROP_DISEASES.get(crop, ["healthy"])
        
        # Create fallback model if needed
        if self.use_pretrained_fallback and not self.disease_models:
            self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create a generic disease classification model for dev/testing"""
        print("📦 Creating fallback disease classifier (fine-tune for production)")
        
        # Simple CNN for disease classification
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(10, activation='softmax')  # Max 10 diseases per crop
        ])
        
        # Use same model for all crops in fallback mode
        for crop in self.disease_labels.keys():
            self.disease_models[crop] = model
        
        self.model_version = "fallback-cnn"
    
    def preprocess_image(
        self, 
        image_bytes: bytes, 
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """Convert bytes to normalized tensor"""
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img_array = np.array(img) / 255.0
        return img_array.astype(np.float32)
    
    def diagnose_disease(
        self,
        image_bytes: bytes,
        detected_crop: str,
        valid_diseases: List[str]
    ) -> Dict:
        """
        CONTEXT-AWARE disease diagnosis.
        
        - ONLY checks diseases valid for detected_crop
        - Calculates REAL severity via lesion segmentation
        - Returns DYNAMIC remedies based on context
        
        Args:
            image_bytes: Raw image bytes
            detected_crop: Crop type from crop detector
            valid_diseases: List of diseases valid for this crop
            
        Returns:
            {disease, confidence, severity_percent, remedies, urgency, ...}
        """
        start_time = time.time()
        
        # Check if we have a model for this crop
        if detected_crop not in self.disease_models:
            return self._no_model_response(detected_crop)
        
        model = self.disease_models[detected_crop]
        labels = self.disease_labels.get(detected_crop, ["healthy"])
        
        # Preprocess and run inference
        img_tensor = self.preprocess_image(image_bytes)
        predictions = model.predict(
            np.expand_dims(img_tensor, axis=0), 
            verbose=0
        )
        
        # Get top prediction
        disease_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][disease_idx])
        
        # Map index to disease name
        if disease_idx < len(labels):
            disease_name = labels[disease_idx]
        else:
            disease_name = "unknown"
        
        # CRITICAL: Validate against valid diseases list
        detection_method = "ai_inference"
        
        if confidence < 0.65:
            # Low confidence → default to healthy
            disease_name = "healthy"
            confidence = 1.0 - confidence
            detection_method = "low_confidence_fallback"
        elif disease_name not in valid_diseases and disease_name != "healthy":
            # Disease not valid for this crop → mark healthy
            disease_name = "healthy"
            confidence = 0.7
            detection_method = "invalid_disease_fallback"
        
        # Calculate REAL severity using OpenCV (only for diseased crops)
        severity_percent = 0.0
        lesion_analysis = None
        
        if disease_name != "healthy":
            severity_percent, lesion_analysis = self.calculate_lesion_severity(
                image_bytes, 
                disease_name
            )
        
        # Generate context-aware remedies
        remedies = self.generate_contextual_remedies(
            detected_crop, 
            disease_name, 
            severity_percent
        )
        
        # Determine urgency level
        urgency = self.determine_urgency(severity_percent, disease_name)
        
        inference_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "disease": disease_name,
            "confidence": round(confidence, 4),
            "severity_percent": round(severity_percent, 2),
            "urgency": urgency,
            "remedies": remedies,
            "lesion_analysis": lesion_analysis,
            "detection_method": detection_method,
            "valid_for_crop": disease_name in valid_diseases or disease_name == "healthy",
            "inference_time_ms": inference_time_ms,
            "model_version": self.model_version
        }
    
    def calculate_lesion_severity(
        self, 
        image_bytes: bytes, 
        disease_type: str
    ) -> Tuple[float, Dict]:
        """
        REAL severity analysis via OpenCV segmentation.
        
        Returns: (severity_percent, analysis_details)
        """
        # Convert bytes to OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return 0.0, {"error": "Failed to decode image"}
        
        # Convert to HSV for color-based segmentation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Get disease-specific color profile
        profile = self._get_disease_color_profile(disease_type)
        lower = np.array(profile["lower"])
        upper = np.array(profile["upper"])
        
        # Create mask for lesion areas
        mask = cv2.inRange(hsv, lower, upper)
        
        # Apply morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Calculate leaf area (green regions)
        leaf_lower = np.array([35, 40, 40])
        leaf_upper = np.array([85, 255, 255])
        leaf_mask = cv2.inRange(hsv, leaf_lower, leaf_upper)
        leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_CLOSE, kernel)
        
        # Calculate areas
        total_pixels = img.shape[0] * img.shape[1]
        leaf_pixels = max(cv2.countNonZero(leaf_mask), total_pixels * 0.3)  # Min 30% assumed leaf
        lesion_pixels = cv2.countNonZero(mask)
        
        # Calculate severity as percentage of leaf area
        severity = (lesion_pixels / leaf_pixels) * 100
        severity = min(max(severity, 0.0), 95.0)  # Clamp to realistic range
        
        # Find contours for lesion count
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        significant_lesions = [c for c in contours if cv2.contourArea(c) > 100]
        
        # Calculate average lesion size
        avg_lesion_size = 0
        if significant_lesions:
            avg_lesion_size = np.mean([cv2.contourArea(c) for c in significant_lesions])
        
        analysis = {
            "lesion_count": len(significant_lesions),
            "lesion_pixels": int(lesion_pixels),
            "leaf_pixels": int(leaf_pixels),
            "avg_lesion_size_px": round(avg_lesion_size, 1),
            "color_profile_used": profile["type"],
            "detection_method": "opencv_hsv_segmentation"
        }
        
        return severity, analysis
    
    def _get_disease_color_profile(self, disease_type: str) -> Dict:
        """Get HSV color range for disease type"""
        # Check for exact match first
        if disease_type in DISEASE_COLOR_PROFILES:
            return DISEASE_COLOR_PROFILES[disease_type]
        
        # Check for partial matches
        for key, profile in DISEASE_COLOR_PROFILES.items():
            if key in disease_type.lower() or disease_type.lower() in key:
                return profile
        
        return DISEASE_COLOR_PROFILES["default"]
    
    def generate_contextual_remedies(
        self, 
        crop: str, 
        disease: str, 
        severity: float
    ) -> Dict:
        """
        Generate DYNAMIC remedies based on crop + disease + severity context.
        NOT static text - adjusts recommendations based on severity.
        """
        key = f"{crop}_{disease}"
        
        result = {
            "organic": [],
            "chemical": [],
            "prevention": [],
            "immediate_actions": [],
            "severity_note": ""
        }
        
        if disease == "healthy":
            result["organic"] = ["Continue regular monitoring", "Maintain current practices"]
            result["prevention"] = ["Regular field inspection recommended"]
            return result
        
        if key in REMEDY_DB:
            remedies = REMEDY_DB[key]
            
            # Always include organic remedies
            result["organic"] = remedies.get("organic", [])[:3]  # Top 3
            
            # Add prevention tips
            result["prevention"] = remedies.get("prevention", [])
            
            # Chemical remedies based on severity
            if severity > 30:
                result["chemical"] = remedies.get("chemical", [])
                result["severity_note"] = "Moderate infection - consider integrated management"
            
            # Add immediate actions for high severity
            if severity > 50:
                result["immediate_actions"] = [
                    "⚠️ URGENT: Remove and destroy heavily infected plant parts",
                    "Isolate affected area to prevent spread",
                    "Apply recommended fungicide/bactericide immediately"
                ]
                result["severity_note"] = "⚠️ SEVERE - Immediate action required"
            
            if severity > 70:
                result["immediate_actions"].append(
                    "🚨 CRITICAL: Contact agricultural extension officer within 24 hours"
                )
        else:
            # Fallback for unknown disease combinations
            result["organic"] = [
                f"Apply broad-spectrum organic fungicide",
                "Remove infected plant material",
                "Improve air circulation around plants"
            ]
            result["prevention"] = ["Consult local agricultural expert for specific recommendations"]
        
        return result
    
    def determine_urgency(self, severity: float, disease: str) -> str:
        """Determine action urgency based on severity and disease type"""
        if disease == "healthy":
            return "none"
        
        # Some diseases spread faster
        fast_spreading = ["late_blight", "blast", "rust", "leaf_curl"]
        is_fast_spreading = any(d in disease.lower() for d in fast_spreading)
        
        if severity > 60 or (severity > 40 and is_fast_spreading):
            return "critical"
        if severity > 30 or (severity > 20 and is_fast_spreading):
            return "high"
        if severity > 15:
            return "medium"
        return "low"
    
    def _no_model_response(self, crop: str) -> Dict:
        """Response when no model available for crop"""
        return {
            "disease": "model_not_available",
            "confidence": 0.0,
            "severity_percent": 0.0,
            "urgency": "unknown",
            "remedies": {
                "organic": [],
                "chemical": [],
                "prevention": [],
                "immediate_actions": [f"No disease model available for {crop}"]
            },
            "detection_method": "no_model",
            "model_version": None
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================
_detector_instance: Optional[DiseaseDetector] = None

def get_disease_detector() -> DiseaseDetector:
    """Get or create singleton DiseaseDetector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = DiseaseDetector(use_pretrained_fallback=True)
    return _detector_instance


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================
def diagnose_disease(
    image_bytes: bytes, 
    detected_crop: str, 
    valid_diseases: List[str]
) -> Dict:
    """
    Convenience function for disease diagnosis.
    
    Usage:
        from ai_models.disease_detector import diagnose_disease
        result = diagnose_disease(image_bytes, "tomato", ["healthy", "early_blight", "late_blight"])
    """
    detector = get_disease_detector()
    return detector.diagnose_disease(image_bytes, detected_crop, valid_diseases)


def calculate_severity(image_bytes: bytes, disease_type: str) -> Tuple[float, Dict]:
    """Calculate lesion severity using OpenCV"""
    detector = get_disease_detector()
    return detector.calculate_lesion_severity(image_bytes, disease_type)
