"""
AgroGrade AI Backend - Main Application Entry Point
FastAPI application with PostgreSQL integration
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.config import settings
from app.database import init_db, close_db
from app.routes import ai_pipeline, crops


# =============================================================================
# LOGGING SETUP
# =============================================================================
logger.remove()
logger.add(sys.stdout, level=settings.log_level, colorize=True)
logger.add(settings.log_file, level=settings.log_level, rotation="10 MB")


# =============================================================================
# APPLICATION LIFESPAN
# =============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # STARTUP
    logger.info("🚀 Starting AgroGrade AI Engine...")
    logger.info(f"📍 Environment: {settings.environment}")
    logger.info(f"🗄️ Database: {settings.database_url.split('@')[-1]}")  # Hide password
    
    # Initialize database
    try:
        await init_db()
        logger.success("✅ Database connected successfully!")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise
    
    yield  # Application runs here
    
    # SHUTDOWN
    logger.info("🔌 Shutting down AgroGrade AI Engine...")
    await close_db()
    logger.info("👋 Goodbye!")


# =============================================================================
# CREATE APPLICATION
# =============================================================================
app = FastAPI(
    title=settings.app_name,
    description="""
    🌾 **AgroGrade AI Engine** - Agricultural Intelligence Platform
    
    Real-time AI-powered crop analysis for Indian farmers:
    
    * 🔬 **Disease Scanner** - Upload leaf images for instant AI diagnosis
    * 📊 **Quality Grader** - Get A/B/C grades with Trust Tags
    * 🌡️ **Sensor Fusion** - Combine IoT data with visual analysis
    * 🛒 **Marketplace Ready** - Verified quality for direct sales
    
    ---
    
    **Supported Crops:** Cotton, Wheat, Rice, Tomato, Potato, Okra, Chilli, Onion
    
    **Regions:** Gujarat, Punjab, Tamil Nadu, Maharashtra, Karnataka, Andhra Pradesh
    """,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# =============================================================================
# MIDDLEWARE
# =============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# ROUTES
# =============================================================================
app.include_router(ai_pipeline.router, prefix="/api", tags=["AI Pipeline"])
app.include_router(crops.router, prefix="/api", tags=["Crops & Diseases"])

# TODO: Add more routers
# from app.routes import auth, farmers, marketplace, sensors
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(farmers.router, prefix="/api/farmers", tags=["Farmers"])
# app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
# app.include_router(sensors.router, prefix="/api/sensors", tags=["IoT Sensors"])


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================
@app.get("/", tags=["Root"])
async def root():
    """
    🏠 API Root
    
    Welcome message and links to documentation.
    """
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    ❤️ Health Check
    
    Verify API and database connectivity.
    """
    from app.database import async_engine
    from sqlalchemy import text
    
    db_connected = True
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        db_connected = False
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "ai_ready": True,
        "database_connected": db_connected,
        "version": settings.app_version,
        "environment": settings.environment
    }


# =============================================================================
# RUN WITH UVICORN
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
