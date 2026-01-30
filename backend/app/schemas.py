"""
AgroGrade AI Backend - Pydantic Schemas
Request/Response validation and serialization
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
import uuid


# =============================================================================
# BASE SCHEMAS
# =============================================================================
class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# FARMER SCHEMAS
# =============================================================================
class FarmerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    farm_size_acres: Optional[float] = Field(None, ge=0)
    primary_crops: Optional[List[str]] = None


class FarmerCreate(FarmerBase):
    """Schema for creating a new farmer"""
    password: str = Field(..., min_length=6)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class FarmerUpdate(BaseModel):
    """Schema for updating farmer profile"""
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    farm_size_acres: Optional[float] = None
    primary_crops: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FarmerResponse(FarmerBase, BaseSchema):
    """Schema for farmer response"""
    id: uuid.UUID
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class FarmerLogin(BaseModel):
    """Schema for login request"""
    phone: str
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    farmer: FarmerResponse


# =============================================================================
# AI INFERENCE SCHEMAS
# =============================================================================
class SensorDataInput(BaseModel):
    """Schema for IoT sensor data input"""
    soil_moisture: Optional[float] = Field(None, ge=0, le=100)
    soil_temperature: Optional[float] = None
    nitrogen_ppm: Optional[float] = Field(None, ge=0)
    phosphorus_ppm: Optional[float] = Field(None, ge=0)
    potassium_ppm: Optional[float] = Field(None, ge=0)
    ph_level: Optional[float] = Field(None, ge=0, le=14)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    sensor_timestamp: Optional[datetime] = None


class InsightItem(BaseModel):
    """Schema for a single insight"""
    type: str = Field(..., pattern="^(alert|recommendation|info|warning)$")
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    message: str


class RemedyItem(BaseModel):
    """Schema for a remedy recommendation"""
    type: str = Field(..., pattern="^(organic|chemical|prevention|nutrition)$")
    name: str
    instructions: str


class AIInferenceRequest(BaseModel):
    """Schema for AI inference request (image analysis)"""
    sensor_data: Optional[SensorDataInput] = None


class AIInferenceResponse(BaseSchema):
    """Schema for AI inference response"""
    id: uuid.UUID
    farmer_id: uuid.UUID
    
    # Image info
    image_url: str
    image_hash: str
    
    # Crop detection
    detected_crop: str
    crop_confidence: float = Field(..., ge=0, le=1)
    
    # Disease diagnosis
    disease: Optional[str] = None
    disease_confidence: Optional[float] = Field(None, ge=0, le=1)
    severity_percent: Optional[float] = Field(None, ge=0, le=100)
    is_healthy: bool
    
    # Quality grading
    grade: Optional[str] = None
    grade_score: Optional[float] = Field(None, ge=0, le=100)
    
    # Trust metrics
    trust_score: Optional[float] = Field(None, ge=0, le=100)
    price_multiplier: float = 1.0
    
    # Dynamic insights and remedies
    insights: List[InsightItem] = []
    remedies: Optional[List[RemedyItem]] = None
    
    # Metadata
    inference_time_ms: Optional[int] = None
    model_version: Optional[str] = None
    created_at: datetime


class InferenceListResponse(BaseModel):
    """Schema for paginated inference list"""
    items: List[AIInferenceResponse]
    total: int
    page: int
    page_size: int


# =============================================================================
# CROP DISEASE SCHEMAS
# =============================================================================
class CropDiseaseBase(BaseModel):
    crop: str
    disease: str
    scientific_name: Optional[str] = None
    symptoms: Optional[List[str]] = None
    organic_remedies: List[str]
    chemical_remedies: Optional[List[str]] = None
    prevention_tips: Optional[List[str]] = None
    severity_thresholds: dict = {"low": 15, "medium": 40, "high": 60}
    spread_risk: Optional[str] = None
    treatment_duration_days: Optional[int] = None


class CropDiseaseCreate(CropDiseaseBase):
    """Schema for creating a crop disease entry"""
    pass


class CropDiseaseResponse(CropDiseaseBase, BaseSchema):
    """Schema for crop disease response"""
    id: uuid.UUID
    created_at: datetime


# =============================================================================
# MARKETPLACE SCHEMAS
# =============================================================================
class ListingBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    crop_type: str
    variety: Optional[str] = None
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., pattern="^(kg|quintal|ton|piece|dozen)$")
    price_per_unit: float = Field(..., gt=0)
    minimum_order: Optional[float] = Field(None, gt=0)
    district: Optional[str] = None
    state: Optional[str] = None


class ListingCreate(ListingBase):
    """Schema for creating a marketplace listing"""
    images: List[str] = Field(..., min_length=1)
    inference_id: Optional[uuid.UUID] = None


class ListingUpdate(BaseModel):
    """Schema for updating a listing"""
    title: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    price_per_unit: Optional[float] = None
    minimum_order: Optional[float] = None
    status: Optional[str] = None


class ListingResponse(ListingBase, BaseSchema):
    """Schema for marketplace listing response"""
    id: uuid.UUID
    farmer_id: uuid.UUID
    inference_id: Optional[uuid.UUID] = None
    images: List[str]
    grade: Optional[str] = None
    trust_score: Optional[float] = None
    is_verified: bool
    verification_date: Optional[datetime] = None
    status: str
    views_count: int
    inquiries_count: int
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    
    # Include farmer info
    farmer: Optional[FarmerResponse] = None


class ListingListResponse(BaseModel):
    """Schema for paginated listing response"""
    items: List[ListingResponse]
    total: int
    page: int
    page_size: int


# =============================================================================
# IOT SENSOR SCHEMAS
# =============================================================================
class SensorBase(BaseModel):
    device_id: str
    sensor_type: str = Field(..., pattern="^(soil|weather|crop_monitor)$")
    field_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SensorCreate(SensorBase):
    """Schema for registering a new sensor"""
    pass


class SensorResponse(SensorBase, BaseSchema):
    """Schema for sensor response"""
    id: uuid.UUID
    farmer_id: uuid.UUID
    is_active: bool
    last_reading_at: Optional[datetime] = None
    battery_level: Optional[int] = None
    firmware_version: Optional[str] = None
    created_at: datetime


class SensorReadingCreate(BaseModel):
    """Schema for creating a sensor reading"""
    soil_moisture: Optional[float] = None
    soil_temperature: Optional[float] = None
    nitrogen_ppm: Optional[float] = None
    phosphorus_ppm: Optional[float] = None
    potassium_ppm: Optional[float] = None
    ph_level: Optional[float] = None
    air_temperature: Optional[float] = None
    humidity: Optional[float] = None
    rainfall_mm: Optional[float] = None
    wind_speed: Optional[float] = None
    raw_data: Optional[dict] = None


class SensorReadingResponse(SensorReadingCreate, BaseSchema):
    """Schema for sensor reading response"""
    id: uuid.UUID
    sensor_id: uuid.UUID
    recorded_at: datetime


# =============================================================================
# COMMON RESPONSE SCHEMAS
# =============================================================================
class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    ai_ready: bool
    database_connected: bool
    version: str
