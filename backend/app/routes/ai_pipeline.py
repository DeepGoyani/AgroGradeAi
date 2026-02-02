"""
AgroGrade AI - Production-Ready FastAPI Pipeline Endpoint
Orchestrates ENTIRE AI pipeline in ONE call:
Crop Detection → Disease Diagnosis → Quality Grading → Sensor Fusion
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import uuid
import json
import hashlib
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ai_models.crop_detector import detect_crop, get_supported_crops
from ai_models.disease_detector import diagnose_disease
from ai_models.quality_grader import grade_produce
from ai_models.sensor_fusion_engine import calculate_trust_score

router = APIRouter(prefix="/ai", tags=["AI Pipeline"])


# =============================================================================
# PYDANTIC MODELS
# =============================================================================
class SensorData(BaseModel):
    """IoT sensor data from field devices"""
    moisture: Optional[float] = Field(None, ge=0, le=100, description="Soil moisture %")
    npk: Optional[Dict[str, float]] = Field(None, description="NPK values {n, p, k}")
    temperature: Optional[float] = Field(None, ge=-10, le=60, description="Temperature °C")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Air humidity %")
    ph: Optional[float] = Field(None, ge=0, le=14, description="Soil pH")
    location: Optional[Dict[str, float]] = Field(None, description="GPS {lat, lng}")


class AnalysisResponse(BaseModel):
    """Complete AI analysis response"""
    inference_id: str
    timestamp: str
    pipeline_status: str
    processing_time_ms: int
    crop_detection: Dict[str, Any]
    disease_diagnosis: Dict[str, Any]
    quality_grade: Dict[str, Any]
    trust_analysis: Dict[str, Any]
    market_intelligence: Dict[str, Any]
    ai_confidence: Dict[str, Any]


class QuickScanResponse(BaseModel):
    """Simplified response for quick scans"""
    crop: str
    grade: str
    disease: str
    trust_score: float
    market_ready: bool
    top_insight: str


# =============================================================================
# MAIN PIPELINE ENDPOINT
# =============================================================================
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_agricultural_input(
    image: UploadFile = File(..., description="Crop/harvest image (JPG/PNG/WEBP)"),
    sensor_data: Optional[str] = Form(None, description="JSON string of sensor readings"),
    farmer_id: Optional[str] = Form(None, description="Farmer ID for record keeping"),
    save_to_db: bool = Form(True, description="Save inference to database")
):
    """
    🌾 **Complete AI Analysis Pipeline**
    
    Performs real-time analysis in one call:
    1. **Crop Detection** - Identifies crop type from image
    2. **Disease Diagnosis** - Detects diseases valid for detected crop
    3. **Quality Grading** - Assigns A/B/C grade with metrics
    4. **Sensor Fusion** - Combines visual + IoT data for Trust Score
    
    Returns DYNAMIC, context-aware insights (NOT pre-defined responses)
    """
    start_time = time.time()
    inference_id = str(uuid.uuid4())
    
    # === VALIDATE IMAGE ===
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image (JPEG, PNG, or WEBP)"
        )
    
    # Read image bytes ONCE (reused across all pipeline stages)
    try:
        image_bytes = await image.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty image file")
        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Image too large (max 10MB)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image: {str(e)}")
    
    # Compute image hash for duplicate detection
    image_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
    
    # === PARSE SENSOR DATA ===
    sensor_json = None
    if sensor_data:
        try:
            sensor_json = json.loads(sensor_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid sensor_data JSON format")
    
    # === PIPELINE STAGE 1: CROP DETECTION ===
    try:
        crop_result = detect_crop(image_bytes)
        detected_crop = crop_result["crop"]
        crop_confidence = crop_result["confidence"]
        valid_diseases = crop_result["valid_diseases"]
        grading_rules = crop_result.get("grading_rules", {})
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Crop detection failed: {str(e)}"
        )
    
    # === PIPELINE STAGE 2: DISEASE DIAGNOSIS (crop-aware) ===
    try:
        disease_result = diagnose_disease(
            image_bytes, 
            detected_crop, 
            valid_diseases
        )
    except Exception as e:
        # Non-fatal - return degraded result
        disease_result = {
            "disease": "analysis_unavailable",
            "confidence": 0.0,
            "severity_percent": 0.0,
            "urgency": "unknown",
            "remedies": {
                "organic": [],
                "chemical": [],
                "immediate_actions": [f"Disease analysis failed: {str(e)}"]
            },
            "detection_method": "error_fallback"
        }
    
    # === PIPELINE STAGE 3: QUALITY GRADING (crop-specific) ===
    try:
        grade_result = grade_produce(
            image_bytes, 
            detected_crop, 
            grading_rules
        )
    except Exception as e:
        # Non-fatal - return degraded result
        grade_result = {
            "crop": detected_crop,
            "grade": "C",
            "score": 40.0,
            "metrics": {"error": str(e)},
            "defect_map": [],
            "defect_count": 0,
            "market_value_per_kg": 15.0,
            "analysis_method": "error_fallback"
        }
    
    # === PIPELINE STAGE 4: SENSOR FUSION ===
    try:
        trust_result = calculate_trust_score(grade_result, sensor_json)
    except Exception as e:
        # Fallback without sensor fusion
        visual_score = grade_result.get("score", 50)
        trust_result = {
            "trust_score": round(visual_score * 0.85, 1),
            "grade": grade_result.get("grade", "C"),
            "components": {
                "visual_grade_score": visual_score,
                "sensor_health_score": 0,
                "weights": {"visual": 1.0, "sensor": 0.0}
            },
            "insights": [{
                "type": "warning", 
                "message": f"Sensor fusion unavailable: {str(e)}",
                "impact": "neutral"
            }],
            "market_ready": visual_score >= 75,
            "market_tier": "unknown",
            "recommended_actions": ["Proceed with visual-only assessment"]
        }
    
    # === CALCULATE OVERALL AI CONFIDENCE ===
    ai_confidence = _calculate_overall_confidence(
        crop_confidence,
        disease_result.get("confidence", 0.5),
        grade_result.get("score", 50)
    )
    
    # === MARKET INTELLIGENCE ===
    market_intel = _generate_market_intelligence(
        detected_crop,
        grade_result,
        trust_result,
        sensor_json
    )
    
    # === REGION VALIDATION ===
    region_appropriate = _is_region_appropriate(detected_crop, sensor_json)
    
    # Calculate processing time
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    # === SAVE TO DATABASE (non-blocking) ===
    if save_to_db:
        try:
            # TODO: Replace with actual database save
            _save_inference_to_db(
                inference_id=inference_id,
                farmer_id=farmer_id or "anonymous",
                image_hash=image_hash,
                crop_result=crop_result,
                disease_result=disease_result,
                grade_result=grade_result,
                trust_result=trust_result,
                sensor_data=sensor_json
            )
        except Exception as e:
            # Non-critical - log but don't fail API
            print(f"⚠️ DB save warning: {e}")
    
    # === RETURN DYNAMIC RESPONSE ===
    return {
        "inference_id": inference_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_status": "success",
        "processing_time_ms": processing_time_ms,
        "crop_detection": {
            "crop": detected_crop,
            "confidence": round(crop_confidence, 4),
            "valid_diseases": valid_diseases,
            "region_appropriate": region_appropriate,
            "inference_time_ms": crop_result.get("inference_time_ms", 0)
        },
        "disease_diagnosis": disease_result,
        "quality_grade": grade_result,
        "trust_analysis": trust_result,
        "market_intelligence": market_intel,
        "ai_confidence": ai_confidence
    }


# =============================================================================
# QUICK SCAN ENDPOINT (Simplified)
# =============================================================================
@router.post("/quick-scan", response_model=QuickScanResponse)
async def quick_scan(
    image: UploadFile = File(..., description="Crop image for quick analysis")
):
    """
    ⚡ **Quick Scan** - Simplified one-line result
    
    Returns: crop, grade, disease, trust_score, market_ready
    """
    # Read image
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(400, "Empty image")
    
    # Run pipeline
    try:
        crop_result = detect_crop(image_bytes)
        disease_result = diagnose_disease(
            image_bytes, 
            crop_result["crop"], 
            crop_result["valid_diseases"]
        )
        grade_result = grade_produce(image_bytes, crop_result["crop"])
        trust_result = calculate_trust_score(grade_result, None)
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")
    
    # Get top insight
    insights = trust_result.get("insights", [])
    top_insight = insights[0]["message"] if insights else "Analysis complete"
    
    return {
        "crop": crop_result["crop"],
        "grade": grade_result["grade"],
        "disease": disease_result["disease"],
        "trust_score": trust_result["trust_score"],
        "market_ready": trust_result["market_ready"],
        "top_insight": top_insight
    }


# =============================================================================
# BATCH ANALYSIS ENDPOINT
# =============================================================================
@router.post("/batch-analyze")
async def batch_analyze(
    images: List[UploadFile] = File(..., description="Multiple images (max 5)"),
    sensor_data: Optional[str] = Form(None)
):
    """
    📦 **Batch Analysis** - Analyze multiple images at once
    
    Max 5 images per request. Returns array of results.
    """
    if len(images) > 5:
        raise HTTPException(400, "Maximum 5 images per batch")
    
    sensor_json = None
    if sensor_data:
        try:
            sensor_json = json.loads(sensor_data)
        except:
            pass
    
    results = []
    for idx, image in enumerate(images):
        try:
            image_bytes = await image.read()
            crop_result = detect_crop(image_bytes)
            disease_result = diagnose_disease(
                image_bytes,
                crop_result["crop"],
                crop_result["valid_diseases"]
            )
            grade_result = grade_produce(image_bytes, crop_result["crop"])
            trust_result = calculate_trust_score(grade_result, sensor_json)
            
            results.append({
                "index": idx,
                "filename": image.filename,
                "status": "success",
                "crop": crop_result["crop"],
                "disease": disease_result["disease"],
                "grade": grade_result["grade"],
                "trust_score": trust_result["trust_score"]
            })
        except Exception as e:
            results.append({
                "index": idx,
                "filename": image.filename,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "batch_id": str(uuid.uuid4()),
        "total_images": len(images),
        "successful": len([r for r in results if r["status"] == "success"]),
        "results": results
    }


# =============================================================================
# SUPPORTED CROPS ENDPOINT
# =============================================================================
@router.get("/supported-crops")
async def list_supported_crops():
    """
    📋 **List Supported Crops**
    
    Returns all crops the AI can detect and analyze.
    """
    return {
        "supported_crops": get_supported_crops(),
        "total": len(get_supported_crops())
    }


# =============================================================================
# HEALTH CHECK
# =============================================================================
@router.get("/health")
async def ai_pipeline_health():
    """
    ❤️ **AI Pipeline Health Check**
    """
    try:
        # Quick validation that models can be loaded
        from ai_models.crop_detector import get_crop_detector
        from ai_models.disease_detector import get_disease_detector
        from ai_models.quality_grader import get_quality_grader
        
        detector = get_crop_detector()
        
        return {
            "status": "healthy",
            "ai_models_loaded": True,
            "crop_detector": detector.model_loaded,
            "model_version": detector.model_version,
            "supported_crops": len(get_supported_crops())
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def _calculate_overall_confidence(
    crop_conf: float, 
    disease_conf: float, 
    grade_score: float
) -> Dict:
    """Calculate holistic AI confidence score"""
    weights = {"crop": 0.30, "disease": 0.40, "grade": 0.30}
    
    raw_conf = (
        crop_conf * weights["crop"] + 
        disease_conf * weights["disease"] + 
        (grade_score / 100) * weights["grade"]
    )
    
    # Penalty if any stage has very low confidence
    min_stage = min(crop_conf, disease_conf, grade_score / 100)
    if min_stage < 0.4:
        raw_conf *= 0.80
    elif min_stage < 0.6:
        raw_conf *= 0.90
    
    reliability = "high" if raw_conf > 0.80 else "medium" if raw_conf > 0.60 else "low"
    
    return {
        "overall": round(raw_conf * 100, 1),
        "stage_confidences": {
            "crop_detection": round(crop_conf * 100, 1),
            "disease_diagnosis": round(disease_conf * 100, 1),
            "quality_grading": round(grade_score, 1)
        },
        "reliability": reliability,
        "recommendation": (
            "Results are highly reliable" if reliability == "high"
            else "Consider re-scanning with better lighting" if reliability == "medium"
            else "Low confidence - verify with expert"
        )
    }


def _generate_market_intelligence(
    crop: str,
    grade_result: Dict,
    trust_result: Dict,
    sensor_data: Optional[Dict]
) -> Dict:
    """Generate market intelligence based on analysis"""
    # Demand forecasts (simplified)
    demand_map = {
        "tomato": ("high", "Year-round demand in urban markets"),
        "cotton": ("medium", "Seasonal - peak during harvest"),
        "wheat": ("high", "Staple crop - consistent demand"),
        "rice": ("high", "Staple crop - export potential"),
        "okra": ("medium", "Summer vegetable - regional demand"),
        "potato": ("high", "Year-round demand"),
        "chilli": ("medium", "Spice market - quality dependent"),
        "onion": ("high", "Essential commodity - high demand")
    }
    
    demand, demand_note = demand_map.get(crop, ("medium", "Standard market demand"))
    
    market_ready = trust_result.get("market_ready", False)
    trust_score = trust_result.get("trust_score", 50)
    
    # Determine optimal timing
    if market_ready and trust_score >= 85:
        listing_time = "immediate"
        listing_note = "Premium quality - list now for best prices"
    elif market_ready:
        listing_time = "within_24h"
        listing_note = "Good quality - suitable for standard markets"
    else:
        listing_time = "after_remediation"
        listing_note = "Address issues before listing"
    
    # Buyer recommendations
    if trust_score >= 85:
        buyers = ["supermarkets", "export_buyers", "premium_retailers"]
    elif trust_score >= 70:
        buyers = ["fpo_collectives", "apmc_mandis", "wholesale_markets"]
    else:
        buyers = ["local_markets", "processing_units"]
    
    return {
        "estimated_price_per_kg": grade_result.get("market_value_per_kg", 20),
        "demand_level": demand,
        "demand_note": demand_note,
        "optimal_listing_time": listing_time,
        "listing_recommendation": listing_note,
        "recommended_buyers": buyers,
        "market_tier": trust_result.get("market_tier", "unknown"),
        "price_confidence": "high" if trust_score >= 75 else "medium"
    }


def _is_region_appropriate(crop: str, sensor_data: Optional[Dict]) -> bool:
    """Validate crop matches regional growing patterns"""
    if not sensor_data or "location" not in sensor_data:
        return True  # Can't validate without location
    
    location = sensor_data["location"]
    lat = location.get("lat", 22.0)
    lng = location.get("lng", 73.0)
    
    # Simplified regional validation for India
    # Gujarat region (dry climate)
    if lat >= 20 and lat <= 24 and lng >= 68 and lng <= 75:
        # Cotton, groundnut, wheat suitable; rice less common
        if crop == "rice":
            return False  # Rice uncommon in dry Gujarat
    
    # Punjab region (irrigated)
    if lat >= 29 and lat <= 32:
        # Wheat, rice, cotton all suitable
        return True
    
    # South India
    if lat < 16:
        # Rice, sugarcane, coconut suitable; wheat uncommon
        if crop == "wheat":
            return False
    
    return True


def _save_inference_to_db(
    inference_id: str,
    farmer_id: str,
    image_hash: str,
    crop_result: Dict,
    disease_result: Dict,
    grade_result: Dict,
    trust_result: Dict,
    sensor_data: Optional[Dict]
):
    """
    Save inference to database.
    TODO: Replace with actual SQLAlchemy/asyncpg implementation
    """
    # Placeholder - in production, save to PostgreSQL
    print(f"📝 Saving inference {inference_id} for farmer {farmer_id}")
    print(f"   Crop: {crop_result.get('crop')}, Grade: {grade_result.get('grade')}")
    print(f"   Trust Score: {trust_result.get('trust_score')}")
    
    # In production:
    # from app.database import get_db
    # from app.models import AIInference
    # async with get_db() as db:
    #     inference = AIInference(...)
    #     db.add(inference)
    #     await db.commit()
