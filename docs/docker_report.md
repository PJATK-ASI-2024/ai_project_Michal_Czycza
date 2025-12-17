# Docker Deployment Report - Movie Recommender System

**Projekt:** Content-Based Movie Recommender System  
**Autor:** Michał Czycza  
**Data:** 17 grudnia 2025  
**Zajęcia:** Zajęcia 8 - Dockeryzacja i publikacja

---

## 1. Lista Kontenerów i Ich Funkcji

### Backend API (FastAPI)
- **Kontener:** `ai_backend`
- **Obraz:** `mickelele03/ai_project_backend:latest`
- **Port:** 8000
- **Funkcja:** REST API do rekomendacji filmów
- **Technologie:** FastAPI, Uvicorn, scikit-learn, pandas
- **Model:** TF-IDF + Cosine Similarity (best_model.pkl)
- **Dane:** TMDB 5000 Movies Dataset (4803 filmy)

### Frontend UI (Streamlit)
- **Kontener:** `ai_frontend`
- **Obraz:** `mickelele03/ai_project_frontend:latest`
- **Port:** 8501
- **Funkcja:** Interaktywny interfejs użytkownika
- **Technologie:** Streamlit, requests, pandas
- **Features:** Wyszukiwanie filmów, wyświetlanie rekomendacji, custom CSS

---

## 2. Komendy Docker

### Budowa Obrazów

```bash
# Backend
docker build -t ai_project_backend -f app/Dockerfile .

# Frontend
docker build -t ai_project_frontend -f frontend/Dockerfile .
```

### Uruchomienie Kontenerów

```bash
# Backend (pojedynczy kontener)
docker run -p 8000:8000 --name backend ai_project_backend

# Frontend (pojedynczy kontener)
docker run -p 8501:8501 -e API_BASE_URL=http://localhost:8000 --name frontend ai_project_frontend
```

### Docker Compose (cały stack)

```bash
# Uruchom wszystkie usługi
docker-compose up -d backend frontend

# Zobacz logi
docker-compose logs -f

# Zatrzymaj usługi
docker-compose down

# Sprawdź status
docker-compose ps
```

### Publikacja w DockerHub

```bash
# Zaloguj się
docker login

# Taguj obrazy
docker tag ai_project_backend mickelele03/ai_project_backend:latest
docker tag ai_project_frontend mickelele03/ai_project_frontend:latest

# Push do DockerHub
docker push mickelele03/ai_project_backend:latest
docker push mickelele03/ai_project_frontend:latest
```

---

## 3. Linki do Obrazów Docker

### DockerHub
- **Backend API:** https://hub.docker.com/r/mickelele03/ai_project_backend
- **Frontend UI:** https://hub.docker.com/r/mickelele03/ai_project_frontend

### Użycie Publicznych Obrazów

```bash
# Pobierz obrazy
docker pull mickelele03/ai_project_backend:latest
docker pull mickelele03/ai_project_frontend:latest

# Uruchom
docker run -p 8000:8000 mickelele03/ai_project_backend:latest
docker run -p 8501:8501 -e API_BASE_URL=http://localhost:8000 mickelele03/ai_project_frontend:latest
```

---

## 4. Wdrożenie w Chmurze - Render.com ☁️

### Status: ✅ LIVE

**Backend API:**
- URL: https://movie-recommender-backend-92fi.onrender.com
- Swagger Docs: https://movie-recommender-backend-92fi.onrender.com/docs
- Health Check: https://movie-recommender-backend-92fi.onrender.com/health

**Frontend UI:**
- URL: https://movie-recommender-frontend-92fi.onrender.com
- Status: Aktywny 24/7 (Free tier: może spać po 15 min nieaktywności)

### Test API w Chmurze

```bash
# Health check
curl https://movie-recommender-backend-92fi.onrender.com/health

# Rekomendacje
curl -X POST https://movie-recommender-backend-92fi.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Avatar", "top_n": 5}'
```

### Wdrożenie - Podsumowanie

| Element | Technologia | Status |
|---------|-------------|--------|
| Hosting | Render.com | ✅ Aktywny |
| Backend | Docker + FastAPI | ✅ Live |
| Frontend | Docker + Streamlit | ✅ Live |
| Region | Frankfurt (EU) | ✅ |
| Plan | Free Tier | ✅ |
| SSL | Automatyczny certyfikat | ✅ |
| CI/CD | Auto-deploy z GitHub | ✅ |

---

## 5. Zrzuty Ekranu

### Lokalne Uruchomienie (Docker Desktop)

**Docker Desktop - Lista Kontenerów:**
![Docker Containers](../frontend/screenshots/6.png)

**Backend API - Swagger Documentation (Lokalnie):**
![Backend Local](../frontend/screenshots/1.png)

**Frontend - Interfejs Użytkownika (Lokalnie):**
![Frontend Local](../frontend/screenshots/2.png)

**Frontend - Wyniki Rekomendacji (Lokalnie):**
![Recommendations Local](../frontend/screenshots/3.png)

### Wdrożenie w Chmurze (Render.com)

**Backend API - Swagger na Render:**
- URL: https://movie-recommender-backend-92fi.onrender.com/docs
- Wszystkie endpointy dostępne publicznie

**Frontend UI - Streamlit na Render:**
- URL: https://movie-recommender-frontend-92fi.onrender.com
- Działa identycznie jak lokalna wersja

---


