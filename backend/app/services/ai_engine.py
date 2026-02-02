"""
AgroGrade AI Backend - AI Engine Service
Handles image analysis using TensorFlow models
"""

import io
import random
from typing import Optional, Dict, Any, List
from PIL import Image
import numpy as np

# TensorFlow will be loaded when models are available
# import tensorflow as tf


class AIEngine:
    """
    AI Engine for crop disease detection and quality grading.
    
    This is a MOCK implementation for development.
    In production, replace with actual TensorFlow model inference.
    """
    
    # Supported crops and their common diseases
    CROP_DISEASES = {
        "cotton": ["bacterial_blight", "grey_mildew", "fusarium_wilt", "leaf_curl"],
        "tomato": ["early_blight", "late_blight", "leaf_curl", "septoria_leaf_spot"],
        "wheat": ["rust", "powdery_mildew", "loose_smut", "karnal_bunt"],
        "rice": ["blast", "brown_spot", "sheath_blight", "bacterial_leaf_blight"],
        "potato": ["late_blight", "early_blight", "black_scurf", "common_scab"],
        "okra": ["yellow_vein_mosaic", "powdery_mildew", "cercospora_leaf_spot"],
        "chilli": ["leaf_curl", "anthracnose", "powdery_mildew", "bacterial_wilt"],
        "onion": ["purple_blotch", "stemphylium_blight", "downy_mildew"],
    }
    
    # Default supported crops
    SUPPORTED_CROPS = list(CROP_DISEASES.keys())
    
    def __init__(self):
        self.model_version = "mock-v1.0.0"
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """
        Load TensorFlow models.
        In production, this would load actual model files.
        """
        # TODO: Load actual TensorFlow models
        # self.crop_model = tf.keras.models.load_model(settings.crop_model_path)
        # self.disease_model = tf.keras.models.load_model(settings.disease_model_path)
        # self.quality_model = tf.keras.models.load_model(settings.quality_model_path)
        
        self.models_loaded = True
        print("✅ AI Engine initialized (mock mode)")
    
    async def analyze_image(
        self, 
        image_content: bytes,
        sensor_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze crop image and return inference results.
        
        Args:
            image_content: Raw image bytes
            sensor_data: Optional IoT sensor data for fusion
            
        Returns:
            Dict with crop, disease, grade, insights
        """
        # Open and preprocess image
        image = Image.open(io.BytesIO(image_content))
        image_array = np.array(image)
        
        # Get image characteristics for mock analysis
        avg_green = self._get_green_channel_avg(image_array)
        brightness = self._get_brightness(image_array)
        
        # MOCK: Detect crop (in production, use CNN model)
        detected_crop = self._mock_detect_crop(image_array)
        crop_confidence = random.uniform(0.85, 0.98)
        
        # MOCK: Detect disease (in production, use CNN model)
        is_healthy = random.random() > 0.4  # 60% chance healthy
        disease = None
        disease_confidence = None
        severity_percent = None
        
        if not is_healthy:
            disease = self._mock_detect_disease(detected_crop)
            disease_confidence = random.uniform(0.75, 0.95)
            severity_percent = random.uniform(10, 70)
        
        # Calculate quality grade
        grade, grade_score = self._calculate_grade(
            is_healthy=is_healthy,
            severity=severity_percent,
            brightness=brightness,
            green_ratio=avg_green
        )
        
        # Calculate trust score (with sensor fusion if available)
        trust_score = self._calculate_trust_score(
            crop_confidence=crop_confidence,
            disease_confidence=disease_confidence,
            grade_score=grade_score,
            sensor_data=sensor_data
        )
        
        # Calculate price multiplier based on grade
        price_multiplier = self._get_price_multiplier(grade, trust_score)
        
        # Generate dynamic insights
        insights = self._generate_insights(
            detected_crop=detected_crop,
            disease=disease,
            severity=severity_percent,
            sensor_data=sensor_data,
            grade=grade
        )
        
        return {
            "detected_crop": detected_crop,
            "crop_confidence": round(crop_confidence, 3),
            "disease": disease,
            "disease_confidence": round(disease_confidence, 3) if disease_confidence else None,
            "severity_percent": round(severity_percent, 1) if severity_percent else None,
            "grade": grade,
            "grade_score": round(grade_score, 1),
            "trust_score": round(trust_score, 1),
            "price_multiplier": round(price_multiplier, 2),
            "insights": insights,
            "is_healthy": is_healthy
        }
    
    def _get_green_channel_avg(self, image_array: np.ndarray) -> float:
        """Calculate average green channel value"""
        if len(image_array.shape) >= 3:
            return float(np.mean(image_array[:, :, 1]))  # Green channel
        return 128.0
    
    def _get_brightness(self, image_array: np.ndarray) -> float:
        """Calculate image brightness"""
        return float(np.mean(image_array))
    
    def _mock_detect_crop(self, image_array: np.ndarray) -> str:
        """Mock crop detection based on image characteristics"""
        # In production, use actual CNN model inference
        return random.choice(self.SUPPORTED_CROPS)
    
    def _mock_detect_disease(self, crop: str) -> str:
        """Mock disease detection for a given crop"""
        diseases = self.CROP_DISEASES.get(crop, ["unknown_disease"])
        return random.choice(diseases)
    
    def _calculate_grade(
        self,
        is_healthy: bool,
        severity: Optional[float],
        brightness: float,
        green_ratio: float
    ) -> tuple:
        """Calculate quality grade based on analysis"""
        base_score = 85 if is_healthy else max(30, 80 - (severity or 0))
        
        # Adjust for image quality indicators
        if brightness > 100 and brightness < 200:
            base_score += 5
        if green_ratio > 80 and green_ratio < 180:
            base_score += 5
        
        # Cap at 100
        score = min(100, max(0, base_score + random.uniform(-5, 5)))
        
        # Assign grade
        if score >= 80:
            grade = "A"
        elif score >= 60:
            grade = "B"
        else:
            grade = "C"
        
        return grade, score
    
    def _calculate_trust_score(
        self,
        crop_confidence: float,
        disease_confidence: Optional[float],
        grade_score: float,
        sensor_data: Optional[Dict[str, Any]]
    ) -> float:
        """
        Calculate trust score using AI confidence and sensor fusion.
        Higher score = more reliable quality assessment.
        """
        # Base trust from AI confidence
        ai_trust = crop_confidence * 50  # Max 50 from AI
        
        if disease_confidence:
            ai_trust += (1 - disease_confidence) * 10  # Lower disease = higher trust
        else:
            ai_trust += 10  # Healthy plants get bonus
        
        # Grade contribution
        grade_trust = grade_score * 0.2  # Max 20 from grade
        
        # Sensor fusion bonus
        sensor_trust = 0
        if sensor_data:
            # Good moisture = bonus
            moisture = sensor_data.get("soil_moisture", 50)
            if 40 <= moisture <= 80:
                sensor_trust += 10
            
            # Good NPK levels = bonus
            if sensor_data.get("nitrogen_ppm"):
                sensor_trust += 5
            if sensor_data.get("phosphorus_ppm"):
                sensor_trust += 5
        
        total = ai_trust + grade_trust + sensor_trust
        return min(100, max(0, total))
    
    def _get_price_multiplier(self, grade: str, trust_score: float) -> float:
        """Calculate price multiplier based on grade and trust"""
        base_multipliers = {"A": 1.4, "B": 1.15, "C": 0.9}
        base = base_multipliers.get(grade, 1.0)
        
        # Trust bonus (up to 10% extra)
        trust_bonus = (trust_score - 50) / 500 if trust_score > 50 else 0
        
        return base + trust_bonus
    
    def _generate_insights(
        self,
        detected_crop: str,
        disease: Optional[str],
        severity: Optional[float],
        sensor_data: Optional[Dict[str, Any]],
        grade: str
    ) -> List[Dict[str, Any]]:
        """Generate dynamic insights based on analysis"""
        insights = []
        
        # Disease insights
        if disease:
            severity_level = "low" if (severity or 0) < 30 else "medium" if (severity or 0) < 60 else "high"
            insights.append({
                "type": "alert",
                "severity": severity_level,
                "message": f"{disease.replace('_', ' ').title()} detected on {detected_crop} ({severity:.1f}% coverage)"
            })
            insights.append({
                "type": "recommendation",
                "message": f"Apply organic treatment immediately. Check crop_diseases API for specific remedies."
            })
        else:
            insights.append({
                "type": "info",
                "message": f"Your {detected_crop} crop appears healthy! Continue regular monitoring."
            })
        
        # Sensor-based insights
        if sensor_data:
            moisture = sensor_data.get("soil_moisture")
            if moisture is not None:
                if moisture < 40:
                    insights.append({
                        "type": "warning",
                        "severity": "medium",
                        "message": f"Low soil moisture ({moisture}%). Consider irrigation."
                    })
                elif moisture > 80:
                    insights.append({
                        "type": "warning", 
                        "severity": "low",
                        "message": f"High soil moisture ({moisture}%). Monitor for root diseases."
                    })
                else:
                    insights.append({
                        "type": "info",
                        "message": f"Soil moisture optimal at {moisture}%."
                    })
            
            nitrogen = sensor_data.get("nitrogen_ppm")
            if nitrogen is not None and nitrogen < 30:
                insights.append({
                    "type": "recommendation",
                    "message": f"Nitrogen levels low ({nitrogen} ppm). Consider nitrogen-rich fertilizer."
                })
        
        # Grade insights
        if grade == "A":
            insights.append({
                "type": "info",
                "message": "Premium quality! Eligible for higher market prices with Trust Tag."
            })
        elif grade == "C":
            insights.append({
                "type": "recommendation",
                "message": "Quality below premium. Consider local markets or processing use."
            })
        
        return insights
