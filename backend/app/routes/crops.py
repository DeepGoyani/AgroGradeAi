"""
AgroGrade AI Backend - Crops Routes
Handles crop disease information and remedies
"""

import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct

from app.database import get_db
from app.models import CropDisease
from app.schemas import CropDiseaseResponse, CropDiseaseCreate, MessageResponse

router = APIRouter(tags=["Crops & Diseases"])


# =============================================================================
# CROP ENDPOINTS
# =============================================================================
@router.get("/crops", response_model=List[str])
async def list_supported_crops(
    db: AsyncSession = Depends(get_db)
):
    """
    🌾 List All Supported Crops
    
    Returns list of crops that have disease data in the system.
    """
    result = await db.execute(
        select(distinct(CropDisease.crop)).order_by(CropDisease.crop)
    )
    crops = [row[0] for row in result.all()]
    
    # Add default crops even if no disease data yet
    default_crops = ["cotton", "wheat", "rice", "tomato", "potato", "okra", "chilli", "onion"]
    all_crops = list(set(crops + default_crops))
    all_crops.sort()
    
    return all_crops


@router.get("/crops/{crop}/diseases", response_model=List[CropDiseaseResponse])
async def list_crop_diseases(
    crop: str,
    db: AsyncSession = Depends(get_db)
):
    """
    🦠 List Diseases for a Specific Crop
    
    Get all known diseases, symptoms, and remedies for a crop type.
    """
    result = await db.execute(
        select(CropDisease)
        .where(CropDisease.crop == crop.lower())
        .order_by(CropDisease.disease)
    )
    diseases = result.scalars().all()
    
    if not diseases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No disease data found for crop: {crop}"
        )
    
    return diseases


@router.get("/diseases", response_model=List[CropDiseaseResponse])
async def list_all_diseases(
    crop: Optional[str] = Query(None, description="Filter by crop type"),
    spread_risk: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    📋 List All Diseases
    
    Get paginated list of all crop diseases with optional filters.
    """
    query = select(CropDisease)
    
    if crop:
        query = query.where(CropDisease.crop == crop.lower())
    
    if spread_risk:
        query = query.where(CropDisease.spread_risk == spread_risk)
    
    query = query.order_by(CropDisease.crop, CropDisease.disease)
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    diseases = result.scalars().all()
    
    return diseases


@router.get("/diseases/{disease_id}", response_model=CropDiseaseResponse)
async def get_disease(
    disease_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    🔍 Get Disease Details
    
    Get full details of a specific disease including remedies.
    """
    result = await db.execute(
        select(CropDisease).where(CropDisease.id == disease_id)
    )
    disease = result.scalar_one_or_none()
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )
    
    return disease


@router.get("/diseases/lookup/{crop}/{disease}", response_model=CropDiseaseResponse)
async def lookup_disease(
    crop: str,
    disease: str,
    db: AsyncSession = Depends(get_db)
):
    """
    🔎 Lookup Disease by Crop and Name
    
    Find disease information by crop type and disease name.
    Used by AI engine to get remedies for detected diseases.
    """
    result = await db.execute(
        select(CropDisease)
        .where(CropDisease.crop == crop.lower())
        .where(CropDisease.disease == disease.lower())
    )
    disease_info = result.scalar_one_or_none()
    
    if not disease_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for {disease} on {crop}"
        )
    
    return disease_info


@router.post("/diseases", response_model=CropDiseaseResponse, status_code=status.HTTP_201_CREATED)
async def create_disease(
    disease_data: CropDiseaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    ➕ Add New Disease Data
    
    Add a new crop-disease entry with symptoms and remedies.
    """
    # Check if already exists
    existing = await db.execute(
        select(CropDisease)
        .where(CropDisease.crop == disease_data.crop.lower())
        .where(CropDisease.disease == disease_data.disease.lower())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Disease {disease_data.disease} for {disease_data.crop} already exists"
        )
    
    disease = CropDisease(
        crop=disease_data.crop.lower(),
        disease=disease_data.disease.lower(),
        scientific_name=disease_data.scientific_name,
        symptoms=disease_data.symptoms,
        organic_remedies=disease_data.organic_remedies,
        chemical_remedies=disease_data.chemical_remedies,
        prevention_tips=disease_data.prevention_tips,
        severity_thresholds=disease_data.severity_thresholds,
        spread_risk=disease_data.spread_risk,
        treatment_duration_days=disease_data.treatment_duration_days
    )
    
    db.add(disease)
    await db.commit()
    await db.refresh(disease)
    
    return disease


@router.put("/diseases/{disease_id}", response_model=CropDiseaseResponse)
async def update_disease(
    disease_id: uuid.UUID,
    disease_data: CropDiseaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    ✏️ Update Disease Data
    
    Update disease information, symptoms, or remedies.
    """
    result = await db.execute(
        select(CropDisease).where(CropDisease.id == disease_id)
    )
    disease = result.scalar_one_or_none()
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )
    
    # Update fields
    disease.scientific_name = disease_data.scientific_name
    disease.symptoms = disease_data.symptoms
    disease.organic_remedies = disease_data.organic_remedies
    disease.chemical_remedies = disease_data.chemical_remedies
    disease.prevention_tips = disease_data.prevention_tips
    disease.severity_thresholds = disease_data.severity_thresholds
    disease.spread_risk = disease_data.spread_risk
    disease.treatment_duration_days = disease_data.treatment_duration_days
    
    await db.commit()
    await db.refresh(disease)
    
    return disease


@router.delete("/diseases/{disease_id}", response_model=MessageResponse)
async def delete_disease(
    disease_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    🗑️ Delete Disease Data
    
    Remove a disease entry from the database.
    """
    result = await db.execute(
        select(CropDisease).where(CropDisease.id == disease_id)
    )
    disease = result.scalar_one_or_none()
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )
    
    await db.delete(disease)
    await db.commit()
    
    return MessageResponse(message=f"Disease {disease.disease} deleted successfully")


# =============================================================================
# REMEDY SEARCH
# =============================================================================
@router.get("/remedies/search")
async def search_remedies(
    q: str = Query(..., min_length=2, description="Search query"),
    remedy_type: Optional[str] = Query(None, pattern="^(organic|chemical)$"),
    db: AsyncSession = Depends(get_db)
):
    """
    🔍 Search Remedies
    
    Search for remedies across all crops and diseases.
    """
    result = await db.execute(select(CropDisease))
    all_diseases = result.scalars().all()
    
    search_lower = q.lower()
    matches = []
    
    for disease in all_diseases:
        # Search in organic remedies
        if not remedy_type or remedy_type == "organic":
            for remedy in disease.organic_remedies or []:
                if search_lower in remedy.lower():
                    matches.append({
                        "crop": disease.crop,
                        "disease": disease.disease,
                        "remedy": remedy,
                        "type": "organic"
                    })
        
        # Search in chemical remedies
        if not remedy_type or remedy_type == "chemical":
            for remedy in disease.chemical_remedies or []:
                if search_lower in remedy.lower():
                    matches.append({
                        "crop": disease.crop,
                        "disease": disease.disease,
                        "remedy": remedy,
                        "type": "chemical"
                    })
    
    return {
        "query": q,
        "count": len(matches),
        "results": matches[:50]  # Limit results
    }
