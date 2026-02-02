"""
AgroGrade AI - Enhanced Disease Detector with Trained Model Integration
Integrates trained models into the existing AI pipeline
"""

import os
import json
import io
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import tensorflow as tf
from PIL import Image

# Import existing detector
try:
    from .disease_detector import DiseaseDetector
except ImportError:
    from disease_detector import DiseaseDetector

class EnhancedDiseaseDetector(DiseaseDetector):
    """
    Enhanced disease detector with trained model integration
    """
    
    def __init__(self, use_trained_model: bool = True):
        super().__init__()
        
        self.use_trained_model = use_trained_model
        self.trained_model = None
        self.model_loaded = False
        
        # Load trained model if available
        if use_trained_model:
            self._load_trained_model()
    
    def _load_trained_model(self):
        """Load the trained leaf disease detection model"""
        
        model_path = Path(__file__).parent / "model_weights" / "leaf_disease_classifier.h5"
        metadata_path = Path(__file__).parent / "model_weights" / "model_metadata.json"
        
        if model_path.exists():
            try:
                # Load model
                self.trained_model = tf.keras.models.load_model(str(model_path))
                
                # Load metadata
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        self.model_metadata = json.load(f)
                    self.class_names = self.model_metadata['class_names']
                    self.num_classes = self.model_metadata['num_classes']
                else:
                    # Default class names if metadata not found
                    self.class_names = [
                        'healthy_leaf', 'bacterial_blight', 'powdery_mildew',
                        'leaf_spot', 'rust', 'anthracnose', 'mosaic_virus', 'curling'
                    ]
                    self.num_classes = len(self.class_names)
                
                self.model_loaded = True
                print(f"✅ Loaded trained disease detection model")
                print(f"🎯 Classes: {', '.join(self.class_names)}")
                
            except Exception as e:
                print(f"⚠️ Failed to load trained model: {e}")
                self.use_trained_model = False
        else:
            print("⚠️ Trained model not found, using fallback methods")
            self.use_trained_model = False
    
    def preprocess_image_for_model(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for trained model inference
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Preprocessed image tensor
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert('RGB')
            
            # Resize to model input size
            image = image.resize((224, 224))
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Normalize (same as training)
            image_array = image_array.astype(np.float32) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            print(f"⚠️ Error preprocessing image: {e}")
            return None
    
    def predict_with_trained_model(self, image_bytes: bytes) -> Dict:
        """
        Make prediction using trained model
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Prediction results
        """
        if not self.model_loaded or not self.trained_model:
            return None
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image_for_model(image_bytes)
            if processed_image is None:
                return None
            
            # Make prediction
            start_time = time.time()
            predictions = self.trained_model.predict(processed_image, verbose=0)
            inference_time = (time.time() - start_time) * 1000
            
            # Process predictions
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            predicted_class = self.class_names[predicted_class_idx]
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_3_predictions = []
            
            for idx in top_3_indices:
                class_name = self.class_names[idx]
                class_confidence = float(predictions[0][idx])
                top_3_predictions.append({
                    "class": class_name,
                    "confidence": round(class_confidence, 4)
                })
            
            # Determine severity based on disease type and confidence
            severity = self._calculate_disease_severity(predicted_class, confidence)
            
            # Get remedy information
            remedy = self._get_disease_remedy(predicted_class)
            
            return {
                "disease": predicted_class,
                "confidence": round(confidence, 4),
                "severity": severity,
                "top_predictions": top_3_predictions,
                "remedy": remedy,
                "inference_time_ms": int(inference_time),
                "model_type": "trained_cnn",
                "class_probabilities": {
                    self.class_names[i]: float(predictions[0][i]) 
                    for i in range(len(self.class_names))
                }
            }
            
        except Exception as e:
            print(f"⚠️ Error in trained model prediction: {e}")
            return None
    
    def _calculate_disease_severity(self, disease: str, confidence: float) -> str:
        """
        Calculate disease severity based on type and confidence
        
        Args:
            disease: Predicted disease class
            confidence: Model confidence
            
        Returns:
            Severity level (low, medium, high, critical)
        """
        if disease == 'healthy_leaf':
            return 'low'
        
        # Base severity by disease type
        disease_severity = {
            'powdery_mildew': 'medium',
            'leaf_spot': 'medium',
            'rust': 'medium',
            'bacterial_blight': 'high',
            'anthracnose': 'high',
            'mosaic_virus': 'critical',
            'curling': 'high'
        }
        
        base_severity = disease_severity.get(disease, 'medium')
        
        # Adjust based on confidence
        if confidence >= 0.9:
            return base_severity
        elif confidence >= 0.7:
            return base_severity if base_severity == 'low' else 'medium'
        else:
            return 'low'
    
    def _get_disease_remedy(self, disease: str) -> Dict:
        """
        Get remedy information for predicted disease
        
        Args:
            disease: Disease class name
            
        Returns:
            Remedy information
        """
        remedies = {
            'healthy_leaf': {
                'action': 'Continue monitoring',
                'treatment': 'Maintain current agricultural practices',
                'prevention': 'Regular crop monitoring and proper irrigation'
            },
            'bacterial_blight': {
                'action': 'Immediate treatment required',
                'treatment': 'Apply copper-based bactericides, remove infected plants',
                'prevention': 'Use disease-resistant varieties, proper drainage'
            },
            'powdery_mildew': {
                'action': 'Treat with fungicides',
                'treatment': 'Apply sulfur-based fungicides, improve air circulation',
                'prevention': 'Proper spacing, resistant varieties'
            },
            'leaf_spot': {
                'action': 'Apply fungicide treatment',
                'treatment': 'Copper fungicides, remove infected leaves',
                'prevention': 'Crop rotation, proper sanitation'
            },
            'rust': {
                'action': 'Fungicide application',
                'treatment': 'Systemic fungicides, remove infected plants',
                'prevention': 'Resistant varieties, avoid overhead irrigation'
            },
            'anthracnose': {
                'action': 'Immediate intervention',
                'treatment': 'Benzimidazole fungicides, destroy infected material',
                'prevention': 'Crop rotation, resistant varieties'
            },
            'mosaic_virus': {
                'action': 'Remove infected plants',
                'treatment': 'No cure, remove and destroy infected plants',
                'prevention': 'Control insect vectors, use certified seeds'
            },
            'curling': {
                'action': 'Address environmental stress',
                'treatment': 'Adjust irrigation, check for viral infection',
                'prevention': 'Proper watering, pest control'
            }
        }
        
        return remedies.get(disease, {
            'action': 'Consult agricultural expert',
            'treatment': 'Seek professional advice',
            'prevention': 'Regular monitoring and best practices'
        })
    
    def diagnose_disease(self, image_bytes: bytes, crop_type: str = None) -> Dict:
        """
        Enhanced disease diagnosis with trained model integration
        
        Args:
            image_bytes: Raw image bytes
            crop_type: Type of crop (optional)
            
        Returns:
            Comprehensive disease diagnosis
        """
        start_time = time.time()
        
        # Try trained model first
        if self.use_trained_model and self.model_loaded:
            trained_result = self.predict_with_trained_model(image_bytes)
            
            if trained_result:
                # Enhance with traditional analysis
                traditional_result = super().diagnose_disease(image_bytes, crop_type)
                
                # Combine results
                combined_result = {
                    **trained_result,
                    "traditional_analysis": traditional_result,
                    "analysis_method": "hybrid",
                    "confidence_boost": True,
                    "lesion_analysis": traditional_result.get("lesion_analysis", {}),
                    "color_analysis": traditional_result.get("color_analysis", {})
                }
                
                processing_time = (time.time() - start_time) * 1000
                combined_result["total_processing_time_ms"] = int(processing_time)
                
                return combined_result
        
        # Fallback to traditional method
        return super().diagnose_disease(image_bytes, crop_type)


# Update the disease detector factory
def create_disease_detector(use_trained_model: bool = True) -> EnhancedDiseaseDetector:
    """
    Factory function to create disease detector
    
    Args:
        use_trained_model: Whether to use trained model if available
        
    Returns:
        Disease detector instance
    """
    return EnhancedDiseaseDetector(use_trained_model=use_trained_model)


# Test function
def test_enhanced_detector():
    """Test the enhanced disease detector"""
    
    print("🧪 Testing Enhanced Disease Detector...")
    
    # Create detector
    detector = create_disease_detector(use_trained_model=True)
    
    # Test with a sample image (if available)
    test_image_path = "test_leaf.jpg"
    
    if Path(test_image_path).exists():
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Make prediction
        result = detector.diagnose_disease(image_bytes, "tomato")
        
        print("✅ Prediction Results:")
        print(f"   Disease: {result.get('disease', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.4f}")
        print(f"   Severity: {result.get('severity', 'Unknown')}")
        print(f"   Model Type: {result.get('model_type', 'Unknown')}")
        
        if 'remedy' in result:
            remedy = result['remedy']
            print(f"   Action: {remedy.get('action', 'Unknown')}")
            print(f"   Treatment: {remedy.get('treatment', 'Unknown')}")
        
    else:
        print("⚠️ No test image found. Create a test_leaf.jpg file to test the detector.")
        print("📊 Detector Status:")
        print(f"   Trained Model Loaded: {detector.model_loaded}")
        print(f"   Classes: {detector.num_classes}")
        print(f"   Using Trained Model: {detector.use_trained_model}")


if __name__ == "__main__":
    test_enhanced_detector()
