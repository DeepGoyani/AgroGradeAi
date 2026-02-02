"""
Test the AgroGrade AI Pipeline with a sample image
"""

import requests
import json
from pathlib import Path

def test_ai_pipeline():
    """Test the AI pipeline endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/ai/analyze"
    
    # Try to find a test image (create a simple one if none exists)
    test_image_path = Path("test_leaf.jpg")
    
    if not test_image_path.exists():
        print("📸 No test image found. You need to provide a crop leaf image.")
        print("   Place an image named 'test_leaf.jpg' in the backend directory")
        print("   Supported crops: cotton, wheat, rice, tomato, okra, potato")
        return
    
    try:
        # Prepare the request
        with open(test_image_path, "rb") as f:
            files = {"image": ("test_leaf.jpg", f, "image/jpeg")}
            data = {
                "sensor_data": json.dumps({
                    "moisture": 65.5,
                    "temperature": 28.4,
                    "humidity": 72.3,
                    "npk": {"n": 120, "p": 45, "k": 80}
                }),
                "farmer_id": "test_farmer_001",
                "save_to_db": "true"
            }
            
            print("🚀 Testing AI Pipeline...")
            print(f"📤 Sending image: {test_image_path}")
            print(f"🔗 Endpoint: {url}")
            
            # Make the request
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ AI Analysis Complete!")
                print("\n🌾 RESULTS:")
                print(f"   Crop Detected: {result['crop_detection']['crop']}")
                print(f"   Confidence: {result['crop_detection']['confidence']:.2%}")
                print(f"   Disease: {result['disease_diagnosis']['disease']}")
                print(f"   Severity: {result['disease_diagnosis']['severity']}")
                print(f"   Quality Grade: {result['quality_grade']['grade']}")
                print(f"   Trust Score: {result['trust_analysis']['trust_score']:.1f}/100")
                print(f"   Market Ready: {'✅' if result['trust_analysis']['market_ready'] else '❌'}")
                print(f"   Processing Time: {result['processing_time_ms']}ms")
                
                # Show AI insights
                if 'top_insight' in result:
                    print(f"\n💡 AI Insight: {result['top_insight']}")
                
                print(f"\n📊 Full Response:")
                print(json.dumps(result, indent=2))
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the backend is running on http://localhost:8000")

if __name__ == "__main__":
    test_ai_pipeline()
