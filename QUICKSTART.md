# 🚀 Quick Start Guide - Movie Recommender Web App

## 📋 Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

## 🔧 Installation

### 1. Clone Repository
```powershell
git clone https://github.com/PJATK-ASI-2024/ai_project_Michal_Czycza.git
cd ai_project_Michal_Czycza
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (Backend)
- Streamlit (Frontend)
- scikit-learn, pandas, numpy (ML)
- pytest (Testing)

## 🎬 Running the Application

### Step 1: Start Backend API

Open a terminal and run:

```powershell
uvicorn app.main:app --reload
```

✅ **Backend running at:** http://localhost:8000  
📚 **API Documentation:** http://localhost:8000/docs

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✅ Model and data loaded successfully
```

### Step 2: Start Frontend UI

Open a **NEW terminal** (keep backend running!) and run:

```powershell
streamlit run frontend/app.py
```

✅ **Frontend running at:** http://localhost:8501

Browser should open automatically. If not, navigate to http://localhost:8501

## 🧪 Testing

Run integration tests:

```powershell
pytest tests/test_api.py -v
```

Expected output:
```
======================== 11 passed in 2.34s =========================
```

## 📖 Usage

1. **Enter a movie title** in the search box (e.g., "Avatar", "Inception")
2. **Adjust number of recommendations** using the slider (1-20)
3. **Click "Get Recommendations"**
4. **View similar movies** with similarity scores and details

## 🛠️ Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```powershell
pip install fastapi uvicorn
```

### Model not found

**Problem:** `FileNotFoundError: [Errno 2] No such file or directory: '...best_model.pkl'`

**Solution:** Run Kedro modeling pipeline first:
```powershell
kedro run --pipeline modeling
```

### Frontend can't connect to API

**Problem:** Frontend shows "❌ API Disconnected"

**Solution:**
1. Make sure backend is running on port 8000
2. Check http://localhost:8000 in browser
3. Restart backend: `uvicorn app.main:app --reload`

### Port already in use

**Problem:** `Error: [Errno 10048] Only one usage of each socket address`

**Solution:** Kill process on port 8000:
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

## 📁 Project Structure

```
ai_project_Michal_Czycza/
│
├── app/                      # Backend API
│   ├── __init__.py
│   └── main.py              # FastAPI application
│
├── frontend/                # Frontend UI
│   └── app.py              # Streamlit application
│
├── data/
│   ├── raw/                # TMDB dataset
│   └── reporting/          # Models (best_model.pkl)
│
├── tests/                  # Integration tests
│   └── test_api.py
│
├── docs/                   # Documentation
│   └── webapp_report.md
│
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔗 Useful Links

- **API Docs (Swagger):** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health
- **Frontend UI:** http://localhost:8501

## 📞 Support

For issues, check:
1. `docs/webapp_report.md` - Full documentation
2. GitHub Issues - Report bugs
3. API logs in terminal

---

**Built with ❤️ using FastAPI + Streamlit**
