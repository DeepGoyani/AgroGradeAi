# 🌾 AgroGrade Backend - Setup Guide

This guide walks you through setting up the AgroGrade AI backend with PostgreSQL.

---

## 📋 Prerequisites

Before starting, ensure you have installed:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

---

## 🚀 Step-by-Step Setup

### Step 1: Install PostgreSQL (if not installed)

**Windows:**
1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Set a password for the `postgres` user (remember this!)
4. Leave default port as `5432`
5. Complete installation

**Verify installation:**
```powershell
psql --version
```

---

### Step 2: Create the Database

Open PowerShell and connect to PostgreSQL:

```powershell
# Connect to PostgreSQL (enter your password when prompted)
psql -U postgres
```

In the PostgreSQL prompt, run:

```sql
-- Create the database
CREATE DATABASE agrograde;

-- Create a dedicated user (optional but recommended)
CREATE USER agrograde_user WITH ENCRYPTED PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE agrograde TO agrograde_user;

-- Connect to the new database
\c agrograde

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";  -- For location data (optional)

-- Exit
\q
```

---

### Step 3: Initialize Database Schema

Run the schema file to create all tables:

```powershell
# Navigate to project directory
cd "c:\Users\Deep\OneDrive\Desktop\Parul AgroGrade\AgroGradeAi"

# Run schema file
psql -U postgres -d agrograde -f database/schema.sql
```

You should see output confirming table creation.

---

### Step 4: Set Up Python Environment

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 5: Configure Environment Variables

```powershell
# Copy example env file
copy .env.example .env

# Edit .env file with your settings
notepad .env
```

**Update these values in `.env`:**

```ini
# Database - use your actual password
DATABASE_URL=postgresql://postgres:your_password_here@localhost:5432/agrograde
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:your_password_here@localhost:5432/agrograde

# Generate a secure secret key
SECRET_KEY=your-random-32-character-string-here

# Set environment
ENVIRONMENT=development
DEBUG=True
```

---

### Step 6: Start the Backend Server

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate

# Run the server
python main.py
```

Or use uvicorn directly:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
🚀 Starting AgroGrade AI Engine...
📍 Environment: development
✅ Database connected successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Step 7: Verify Installation

Open your browser and visit:

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API Root |
| http://localhost:8000/docs | Swagger UI (Interactive API docs) |
| http://localhost:8000/health | Health Check |

---

## 🧪 Test the API

### Test Health Check
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "ai_ready": true,
  "database_connected": true,
  "version": "1.0.0"
}
```

### Test Crop Diseases API
```powershell
curl http://localhost:8000/api/crops
```

---

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .env                      # Your local config (gitignored)
├── app/
│   ├── __init__.py
│   ├── config.py             # Settings from env vars
│   ├── database.py           # PostgreSQL connection
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ai_pipeline.py    # /api/scan, /api/inferences
│   │   └── crops.py          # /api/crops, /api/diseases
│   └── services/
│       ├── __init__.py
│       └── ai_engine.py      # AI inference service
└── logs/                     # Log files (auto-created)

database/
└── schema.sql                # PostgreSQL schema
```

---

## 🔌 Connect Frontend to Backend

Update your React frontend to use the backend API:

```typescript
// src/lib/api.ts
const API_BASE_URL = 'http://localhost:8000/api';

export async function scanCrop(image: File, farmerId: string, sensorData?: object) {
  const formData = new FormData();
  formData.append('image', image);
  formData.append('farmer_id', farmerId);
  if (sensorData) {
    formData.append('sensor_data', JSON.stringify(sensorData));
  }
  
  const response = await fetch(`${API_BASE_URL}/scan`, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}

export async function getCropDiseases(crop: string) {
  const response = await fetch(`${API_BASE_URL}/crops/${crop}/diseases`);
  return response.json();
}
```

---

## 🔧 Troubleshooting

### "psql: command not found"
Add PostgreSQL to your PATH:
```powershell
$env:PATH += ";C:\Program Files\PostgreSQL\14\bin"
```

### "FATAL: password authentication failed"
- Verify your password in `.env`
- Check `pg_hba.conf` allows local connections

### "ModuleNotFoundError: No module named 'app'"
Make sure you're in the `backend/` directory when running the server.

### "Connection refused" on port 5432
Start PostgreSQL service:
```powershell
net start postgresql-x64-14
```

---

## 🎉 Next Steps

1. **Test the Scan API** - Use Swagger UI at `/docs`
2. **Add more routes** - Auth, Farmers, Marketplace, Sensors
3. **Train AI models** - Replace mock engine with TensorFlow models
4. **Deploy** - Use Docker + Railway/Render for production

---

## 📞 Support

If you encounter issues, check:
1. PostgreSQL is running
2. `.env` has correct database credentials
3. Virtual environment is activated
4. All dependencies are installed
