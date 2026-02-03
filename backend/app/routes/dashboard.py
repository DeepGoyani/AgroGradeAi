"""
AgroGrade AI - Dashboard API Routes
User statistics and analytics endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

from .auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Database setup
DB_PATH = Path(__file__).parent.parent.parent / "agrograde_users.db"

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/stats")
async def get_dashboard_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user dashboard statistics"""
    try:
        # Mock data for now - in production, this would query actual analysis results
        stats = {
            "totalAnalyses": 156,
            "healthyCrops": 124,
            "diseasedCrops": 32,
            "avgQuality": 78.5,
            "recentAnalyses": [
                {
                    "id": 1,
                    "crop": "Tomato",
                    "disease": "Healthy",
                    "confidence": 92,
                    "quality": 85,
                    "date": "2024-02-03"
                },
                {
                    "id": 2,
                    "crop": "Wheat",
                    "disease": "Leaf Spot",
                    "confidence": 87,
                    "quality": 72,
                    "date": "2024-02-03"
                },
                {
                    "id": 3,
                    "crop": "Cotton",
                    "disease": "Healthy",
                    "confidence": 95,
                    "quality": 88,
                    "date": "2024-02-02"
                },
                {
                    "id": 4,
                    "crop": "Rice",
                    "disease": "Bacterial Blight",
                    "confidence": 91,
                    "quality": 65,
                    "date": "2024-02-02"
                },
                {
                    "id": 5,
                    "crop": "Potato",
                    "disease": "Healthy",
                    "confidence": 89,
                    "quality": 82,
                    "date": "2024-02-01"
                }
            ],
            "cropDistribution": {
                "Tomato": 45,
                "Wheat": 32,
                "Cotton": 28,
                "Rice": 25,
                "Potato": 18,
                "Okra": 8
            },
            "diseaseTrends": [
                {"disease": "Healthy", "count": 124, "trend": "up"},
                {"disease": "Leaf Spot", "count": 18, "trend": "down"},
                {"disease": "Bacterial Blight", "count": 14, "trend": "stable"}
            ]
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard stats: {str(e)}")

@router.get("/analytics")
async def get_analytics(
    period: str = "week",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed analytics data"""
    try:
        # Mock analytics data
        analytics = {
            "period": period,
            "analysisTrend": [
                {"date": "2024-01-28", "count": 12},
                {"date": "2024-01-29", "count": 18},
                {"date": "2024-01-30", "count": 25},
                {"date": "2024-01-31", "count": 22},
                {"date": "2024-02-01", "count": 28},
                {"date": "2024-02-02", "count": 35},
                {"date": "2024-02-03", "count": 16}
            ],
            "qualityDistribution": {
                "A+": 45,
                "A": 62,
                "B+": 38,
                "B": 11
            },
            "topCrops": [
                {"crop": "Tomato", "count": 45, "avgQuality": 82},
                {"crop": "Wheat", "count": 32, "avgQuality": 78},
                {"crop": "Cotton", "count": 28, "avgQuality": 85}
            ],
            "diseaseBreakdown": [
                {"disease": "Healthy", "count": 124, "percentage": 79.5},
                {"disease": "Leaf Spot", "count": 18, "percentage": 11.5},
                {"disease": "Bacterial Blight", "count": 14, "percentage": 9.0}
            ]
        }
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

@router.get("/recommendations")
async def get_recommendations(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get personalized recommendations based on analysis history"""
    try:
        recommendations = [
            {
                "type": "treatment",
                "title": "Apply Organic Fungicide",
                "description": "Based on recent leaf spot detections, consider using organic fungicide treatments",
                "priority": "high",
                "crop": "Tomato"
            },
            {
                "type": "improvement",
                "title": "Optimize Irrigation Schedule",
                "description": "Your soil moisture levels suggest adjusting irrigation timing",
                "priority": "medium",
                "crop": "Wheat"
            },
            {
                "type": "prevention",
                "title": "Preventive Crop Rotation",
                "description": "Consider rotating crops to prevent soil-borne diseases",
                "priority": "low",
                "crop": "General"
            }
        ]
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")
