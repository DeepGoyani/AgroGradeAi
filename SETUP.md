# 🌾 AgroGrade AI - Quick Setup Guide

## 🚀 One-Command Setup

```bash
# Clone and setup in one command
git clone https://github.com/yourusername/agrograde-ai.git
cd agrograde-ai
python init_project.py
python start_servers.py
```

## 📋 What You Get

- ✅ **Backend**: FastAPI server with ML models
- ✅ **Frontend**: React app with agricultural UI  
- ✅ **AI Models**: Disease detection ready to use
- ✅ **Database**: SQLite/PostgreSQL setup
- ✅ **All Dependencies**: Auto-installed

## 🌐 Access Points

After running `start_servers.py`:

- **Frontend**: http://localhost:8080
- **AI Analysis**: http://localhost:8080/ai-analysis  
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Quick Test

1. Open http://localhost:8080/ai-analysis
2. Upload any leaf image
3. Click "Analyze Leaf"
4. Get instant AI disease detection!

## 📦 Manual Setup (If Needed)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend  
```bash
npm install
npm run dev
```

## 🔧 Requirements

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+ (optional, uses SQLite if not found)

## 📞 Need Help?

- 📖 Full docs: [README.md](README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/agrograde-ai/issues)
- 💬 Support: support@agrograde.ai

---

🎉 **Ready to detect crop diseases with AI!** 🌾
