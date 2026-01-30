"""
AgroGrade AI Backend - SQLAlchemy ORM Models
Maps to PostgreSQL tables defined in database/schema.sql
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, String, Text, Float, Boolean, Integer, 
    ForeignKey, DateTime, ARRAY, JSON, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


# =============================================================================
# FARMERS MODEL
# =============================================================================
class Farmer(Base):
    """Farmer user model with location for regional crop patterns"""
    __tablename__ = "farmers"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(Text, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Location - stored as text for simplicity (use PostGIS for production)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    region: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    farm_size_acres: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    primary_crops: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships
    inferences: Mapped[List["AIInference"]] = relationship(
        "AIInference", 
        back_populates="farmer",
        cascade="all, delete-orphan"
    )
    listings: Mapped[List["MarketplaceListing"]] = relationship(
        "MarketplaceListing", 
        back_populates="farmer",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Farmer {self.name} ({self.phone})>"


# =============================================================================
# AI INFERENCE MODEL
# =============================================================================
class AIInference(Base):
    """Stores DYNAMIC AI analysis results"""
    __tablename__ = "ai_inferences"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("farmers.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Image identification
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_hash: Mapped[str] = mapped_column(Text, nullable=False)  # For duplicate detection
    image_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # DYNAMIC Crop Detection
    detected_crop: Mapped[str] = mapped_column(Text, nullable=False)
    crop_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    
    # DYNAMIC Disease Diagnosis (NULL if healthy)
    disease: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disease_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    severity_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Quality Grading
    grade: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    grade_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Trust Score (AI + Sensor fusion)
    trust_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_multiplier: Mapped[float] = mapped_column(Float, default=1.0)
    
    # IoT Sensor Data
    sensor_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # DYNAMIC Insights Array
    insights: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    
    # Recommended Actions
    remedies: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Processing metadata
    inference_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    # Relationships
    farmer: Mapped["Farmer"] = relationship("Farmer", back_populates="inferences")
    
    @property
    def is_healthy(self) -> bool:
        return self.disease is None
    
    def __repr__(self):
        status = "Healthy" if self.is_healthy else f"Disease: {self.disease}"
        return f"<AIInference {self.detected_crop} - {status}>"


# =============================================================================
# CROP DISEASES MODEL
# =============================================================================
class CropDisease(Base):
    """Crop-specific disease mapping for dynamic routing of remedies"""
    __tablename__ = "crop_diseases"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    crop: Mapped[str] = mapped_column(Text, nullable=False)
    disease: Mapped[str] = mapped_column(Text, nullable=False)
    scientific_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    symptoms: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    organic_remedies: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)
    chemical_remedies: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    prevention_tips: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    
    severity_thresholds: Mapped[dict] = mapped_column(
        JSONB, 
        nullable=False,
        default={"low": 15, "medium": 40, "high": 60}
    )
    spread_risk: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    treatment_duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    # Unique constraint
    __table_args__ = (
        CheckConstraint(
            "spread_risk IN ('low', 'medium', 'high')",
            name="valid_spread_risk"
        ),
    )
    
    def __repr__(self):
        return f"<CropDisease {self.crop}/{self.disease}>"


# =============================================================================
# MARKETPLACE LISTING MODEL
# =============================================================================
class MarketplaceListing(Base):
    """Products with AI-verified quality"""
    __tablename__ = "marketplace_listings"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("farmers.id", ondelete="CASCADE"),
        nullable=False
    )
    inference_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("ai_inferences.id"),
        nullable=True
    )
    
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    crop_type: Mapped[str] = mapped_column(Text, nullable=False)
    variety: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Quantity & Pricing
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(Text, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    minimum_order: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Quality verification
    grade: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trust_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    
    # Images
    images: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)
    
    # Location
    district: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(Text, default="active")
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    inquiries_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now()
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    
    # Relationships
    farmer: Mapped["Farmer"] = relationship("Farmer", back_populates="listings")
    
    def __repr__(self):
        return f"<Listing {self.title} - {self.grade} @ ₹{self.price_per_unit}/{self.unit}>"


# =============================================================================
# IOT SENSOR MODEL
# =============================================================================
class IoTSensor(Base):
    """Registered IoT sensors for farms"""
    __tablename__ = "iot_sensors"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("farmers.id", ondelete="CASCADE"),
        nullable=False
    )
    device_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    sensor_type: Mapped[str] = mapped_column(Text, nullable=False)
    
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    field_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_reading_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    battery_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    firmware_version: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    # Relationships
    readings: Mapped[List["SensorReading"]] = relationship(
        "SensorReading", 
        back_populates="sensor",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<IoTSensor {self.device_id} ({self.sensor_type})>"


# =============================================================================
# SENSOR READING MODEL
# =============================================================================
class SensorReading(Base):
    """Time-series data from IoT devices"""
    __tablename__ = "sensor_readings"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    sensor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("iot_sensors.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Soil metrics
    soil_moisture: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    soil_temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    nitrogen_ppm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    phosphorus_ppm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    potassium_ppm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ph_level: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Weather metrics
    air_temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    humidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Raw data
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    # Relationships
    sensor: Mapped["IoTSensor"] = relationship("IoTSensor", back_populates="readings")
    
    def __repr__(self):
        return f"<SensorReading {self.recorded_at}>"
