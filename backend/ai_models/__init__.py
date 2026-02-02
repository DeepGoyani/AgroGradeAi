"""
AgroGrade AI Models Package

Complete AI Pipeline:
1. Crop Detection (crop_detector.py)
2. Disease Diagnosis (disease_detector.py)  
3. Quality Grading (quality_grader.py)
4. Sensor Fusion & Trust Score (sensor_fusion_engine.py)
"""

from ai_models.crop_detector import (
    detect_crop,
    get_crop_detector,
    get_valid_diseases_for_crop,
    get_supported_crops,
    CropDetector,
    CROP_LABELS,
    CROP_DISEASES
)

from ai_models.disease_detector import (
    diagnose_disease,
    get_disease_detector,
    calculate_severity,
    DiseaseDetector,
    REMEDY_DB
)

from ai_models.quality_grader import (
    grade_produce,
    get_quality_grader,
    QualityGrader
)

from ai_models.sensor_fusion_engine import (
    calculate_trust_score,
    get_sensor_fusion_engine,
    fuse_all_data,
    SensorFusionEngine
)

__all__ = [
    # Crop detection
    "detect_crop",
    "get_crop_detector",
    "get_valid_diseases_for_crop",
    "get_supported_crops",
    "CropDetector",
    "CROP_LABELS",
    "CROP_DISEASES",
    # Disease detection
    "diagnose_disease",
    "get_disease_detector",
    "calculate_severity",
    "DiseaseDetector",
    "REMEDY_DB",
    # Quality grading
    "grade_produce",
    "get_quality_grader",
    "QualityGrader",
    # Sensor fusion
    "calculate_trust_score",
    "get_sensor_fusion_engine",
    "fuse_all_data",
    "SensorFusionEngine"
]
