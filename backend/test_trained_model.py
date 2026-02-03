#!/usr/bin/env python3
"""
Test the trained AI model directly
"""

import numpy as np
from PIL import Image
import io
from ai_models.enhanced_disease_detector import EnhancedDiseaseDetector

def create_test_leaf_image():
    """Create a test leaf image with disease symptoms"""
    # Create a 224x224 RGB image
    image = np.ones((224, 224, 3), dtype=np.uint8) * 200  # Light green background
    
    # Add some brown spots to simulate disease
    for _ in range(20):
        x = np.random.randint(20, 204)
        y = np.random.randint(20, 204)
        radius = np.random.randint(3, 8)
        
        # Brown color for disease spots
        image[y-radius:y+radius, x-radius:x+radius] = [139, 69, 19]
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_trained_model():
    """Test the trained disease detection model"""
    print("🧪 Testing Trained Disease Detection Model")
    print("=" * 50)
    
    # Initialize detector
    detector = EnhancedDiseaseDetector(use_trained_model=True)
    
    print(f"📊 Model Status:")
    print(f"   Model Loaded: {detector.model_loaded}")
    print(f"   Using Trained Model: {detector.use_trained_model}")
    
    if not detector.model_loaded:
        print("❌ Trained model not loaded!")
        return
    
    print(f"   Classes: {', '.join(detector.class_names)}")
    
    # Create test image
    print("\n🖼️ Creating test leaf image with disease symptoms...")
    test_image_bytes = create_test_leaf_image()
    
    # Test prediction
    print("\n🔬 Running disease detection...")
    result = detector.predict_with_trained_model(test_image_bytes)
    
    if result:
        print(f"✅ Prediction successful!")
        print(f"🎯 Disease: {result.get('disease_type', 'Unknown')}")
        print(f"📈 Confidence: {result.get('confidence', 0):.2%}")
        print(f"⚠️ Severity: {result.get('severity', 'Unknown')}")
        
        if 'top_predictions' in result:
            print(f"\n🏆 Top 3 Predictions:")
            for i, pred in enumerate(result['top_predictions'][:3], 1):
                print(f"   {i}. {pred['class']} ({pred['confidence']:.2%})")
    else:
        print("❌ Prediction failed!")
    
    # Test full analysis
    print("\n🔍 Testing full analysis pipeline...")
    full_result = detector.analyze_leaf_disease(test_image_bytes, "test_crop")
    
    if full_result:
        print(f"✅ Full analysis successful!")
        print(f"🎯 Primary Disease: {full_result.get('disease_type', 'Unknown')}")
        print(f"📈 Confidence: {full_result.get('confidence', 0):.2%}")
        print(f"⚠️ Severity: {full_result.get('severity', 'Unknown')}")
        print(f"💊 Remedy: {full_result.get('remedy', 'No remedy available')}")
    else:
        print("❌ Full analysis failed!")

if __name__ == "__main__":
    test_trained_model()
