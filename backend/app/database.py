"""
AgroGrade AI Backend - Database Connection Manager
Handles PostgreSQL connections using SQLAlchemy (sync + async)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from app.config import settings

# =============================================================================
# Sync Engine (for migrations and quick scripts)
# =============================================================================
sync_engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

# =============================================================================
# Async Engine (for FastAPI endpoints)
# =============================================================================
async_engine = create_async_engine(
    settings.database_url_async,
    echo=settings.debug,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# =============================================================================
# Base Model for SQLAlchemy ORM
# =============================================================================
Base = declarative_base()


# =============================================================================
# Dependency Injection for FastAPI
# =============================================================================
async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.
    Usage in routes:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """
    Sync database session for scripts and migrations.
    Usage:
        with get_sync_db() as db:
            db.execute(...)
    """
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# =============================================================================
# Database Initialization
# =============================================================================
async def init_db():
    """Initialize database - create all tables"""
    from app.models import Base  # Import models to register them
    
    async with async_engine.begin() as conn:
        # Create tables (for development - use Alembic in production)
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")


async def close_db():
    """Close database connections"""
    await async_engine.dispose()
    print("🔌 Database connections closed.")
