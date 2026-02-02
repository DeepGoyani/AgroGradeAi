"""
AgroGrade AI Backend - AI Pipeline Routes
Handles image upload, AI inference, and results
"""

import uuid
import hashlib
import time
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import AIInference, Farmer, CropDisease
from app.schemas import (
    AIInferenceResponse, 
    InferenceListResponse,
    SensorDataInput,
    MessageResponse
)
from app.services.ai_engine import AIEngine
from app.config import settings

router = APIRouter(tags=["AI Pipeline"])

# Initialize AI Engine (singleton)
ai_engine = AIEngine()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def compute_image_hash(file_content: bytes) -> str:
    """Compute SHA256 hash of image for duplicate detection"""
    return hashlib.sha256(file_content).hexdigest()


async def check_duplicate(db: AsyncSession, image_hash: str, farmer_id: uuid.UUID) -> Optional[AIInference]:
    """Check if this image was already analyzed"""
    result = await db.execute(
        select(AIInference)
        .where(AIInference.image_hash == image_hash)
        .where(AIInference.farmer_id == farmer_id)
        .order_by(desc(AIInference.created_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_remedies_for_disease(db: AsyncSession, crop: str, disease: str) -> Optional[dict]:
    """Get remedies from crop_diseases table"""
    result = await db.execute(
        select(CropDisease)
        .where(CropDisease.crop == crop.lower())
        .where(CropDisease.disease == disease.lower())
    )
    disease_info = result.scalar_one_or_none()
    
    if disease_info:
        remedies = []
        for remedy in disease_info.organic_remedies or []:
            remedies.append({
                "type": "organic",
                "name": remedy,
                "instructions": f"Apply {remedy} as directed"
            })
        for remedy in disease_info.chemical_remedies or []:
            remedies.append({
                "type": "chemical", 
                "name": remedy,
                "instructions": f"Apply {remedy} following manufacturer guidelines"
            })
        return remedies
    return None


# =============================================================================
# AI INFERENCE ENDPOINTS
# =============================================================================
@router.post("/scan", response_model=AIInferenceResponse, status_code=status.HTTP_201_CREATED)
async def scan_crop(
    image: UploadFile = File(..., description="Crop/leaf image to analyze"),
    farmer_id: uuid.UUID = Form(..., description="Farmer ID"),
    sensor_data: Optional[str] = Form(None, description="JSON string of sensor data"),
    db: AsyncSession = Depends(get_db)
):
    """
    🔬 AI Disease Scanner & Quality Grader
    
    Upload a crop/leaf image for real-time AI analysis:
    - Detects crop type (cotton, wheat, rice, tomato, etc.)
    - Diagnoses diseases with confidence scores
    - Grades quality (A/B/C) for marketplace
    - Generates Trust Score with optional sensor fusion
    - Returns dynamic insights and remedies
    """
    start_time = time.time()
    
    # Validate image format
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Read image content
    image_content = await image.read()
    image_size_mb = len(image_content) / (1024 * 1024)
    
    if image_size_mb > settings.max_image_size_mb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image size exceeds {settings.max_image_size_mb}MB limit"
        )
    
    # Compute hash for duplicate detection
    image_hash = compute_image_hash(image_content)
    
    # Check for recent duplicate
    existing = await check_duplicate(db, image_hash, farmer_id)
    if existing:
        # Return cached result if scanned within last hour
        time_diff = datetime.utcnow() - existing.created_at.replace(tzinfo=None)
        if time_diff.total_seconds() < 3600:  # 1 hour
            return existing
    
    # Parse sensor data if provided
    parsed_sensor_data = None
    if sensor_data:
        import json
        try:
            parsed_sensor_data = json.loads(sensor_data)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sensor_data JSON format"
            )
    
    # Run AI inference
    inference_result = await ai_engine.analyze_image(
        image_content=image_content,
        sensor_data=parsed_sensor_data
    )
    
    # Get remedies if disease detected
    remedies = None
    if inference_result.get("disease"):
        remedies = await get_remedies_for_disease(
            db, 
            inference_result["detected_crop"],
            inference_result["disease"]
        )
    
    # Calculate inference time
    inference_time_ms = int((time.time() - start_time) * 1000)
    
    # Save image (in production, upload to cloud storage)
    image_url = f"/uploads/{farmer_id}/{image_hash}.jpg"  # Placeholder
    
    # Create inference record
    inference = AIInference(
        farmer_id=farmer_id,
        image_url=image_url,
        image_hash=image_hash,
        image_metadata={
            "filename": image.filename,
            "content_type": image.content_type,
            "size_bytes": len(image_content)
        },
        detected_crop=inference_result["detected_crop"],
        crop_confidence=inference_result["crop_confidence"],
        disease=inference_result.get("disease"),
        disease_confidence=inference_result.get("disease_confidence"),
        severity_percent=inference_result.get("severity_percent"),
        grade=inference_result.get("grade"),
        grade_score=inference_result.get("grade_score"),
        trust_score=inference_result.get("trust_score"),
        price_multiplier=inference_result.get("price_multiplier", 1.0),
        sensor_data=parsed_sensor_data,
        insights=inference_result.get("insights", []),
        remedies=remedies,
        inference_time_ms=inference_time_ms,
        model_version=ai_engine.model_version
    )
    
    db.add(inference)
    await db.commit()
    await db.refresh(inference)
    
    return inference


@router.get("/inferences", response_model=InferenceListResponse)
async def list_inferences(
    farmer_id: uuid.UUID,
    page: int = 1,
    page_size: int = 20,
    crop: Optional[str] = None,
    disease_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    📋 List AI Inference History
    
    Get paginated list of past scan results for a farmer.
    Filter by crop type or disease-only scans.
    """
    query = select(AIInference).where(AIInference.farmer_id == farmer_id)
    
    if crop:
        query = query.where(AIInference.detected_crop == crop.lower())
    
    if disease_only:
        query = query.where(AIInference.disease.isnot(None))
    
    # Get total count
    count_result = await db.execute(
        select(AIInference.id).where(AIInference.farmer_id == farmer_id)
    )
    total = len(count_result.all())
    
    # Get paginated results
    query = query.order_by(desc(AIInference.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return InferenceListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/inferences/{inference_id}", response_model=AIInferenceResponse)
async def get_inference(
    inference_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    🔍 Get Single Inference Result
    
    Retrieve detailed result of a specific scan.
    """
    result = await db.execute(
        select(AIInference).where(AIInference.id == inference_id)
    )
    inference = result.scalar_one_or_none()
    
    if not inference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inference not found"
        )
    
    return inference


@router.delete("/inferences/{inference_id}", response_model=MessageResponse)
async def delete_inference(
    inference_id: uuid.UUID,
    farmer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    🗑️ Delete Inference Record
    
    Remove a scan result from history.
    """
    result = await db.execute(
        select(AIInference)
        .where(AIInference.id == inference_id)
        .where(AIInference.farmer_id == farmer_id)
    )
    inference = result.scalar_one_or_none()
    
    if not inference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inference not found or not owned by farmer"
        )
    
    await db.delete(inference)
    await db.commit()
    
    return MessageResponse(message="Inference deleted successfully")


@router.get("/stats/{farmer_id}")
async def get_farmer_stats(
    farmer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    📊 Get Farmer AI Statistics
    
    Summary of all scans, disease detections, and grades.
    """
    # Total scans
    total_result = await db.execute(
        select(AIInference).where(AIInference.farmer_id == farmer_id)
    )
    all_inferences = total_result.scalars().all()
    
    total_scans = len(all_inferences)
    disease_count = sum(1 for i in all_inferences if i.disease is not None)
    healthy_count = total_scans - disease_count
    
    # Grade distribution
    grades = {"A": 0, "B": 0, "C": 0}
    for inf in all_inferences:
        if inf.grade in grades:
            grades[inf.grade] += 1
    
    # Crop distribution
    crops = {}
    for inf in all_inferences:
        crops[inf.detected_crop] = crops.get(inf.detected_crop, 0) + 1
    
    # Average trust score
    trust_scores = [i.trust_score for i in all_inferences if i.trust_score]
    avg_trust = sum(trust_scores) / len(trust_scores) if trust_scores else 0
    
    return {
        "total_scans": total_scans,
        "disease_detections": disease_count,
        "healthy_scans": healthy_count,
        "grade_distribution": grades,
        "crop_distribution": crops,
        "average_trust_score": round(avg_trust, 1)
    }
