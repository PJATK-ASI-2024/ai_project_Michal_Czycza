# 🚀 Deployment na Render.com - Instrukcja

## Dlaczego Render.com?

✅ Darmowy tier  
✅ Automatyczna detekcja Dockerfile  
✅ Integracja z GitHub  
✅ Łatwa konfiguracja  
✅ SSL certyfikaty za darmo  
✅ Automatyczne deploymenty przy push  

---

## Metoda 1: Automatyczny Deploy (Blueprint) - NAJŁATWIEJSZA

### Krok 1: Kliknij w Deploy Button

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/PJATK-ASI-2024/ai_project_Michal_Czycza)

### Krok 2: Zaloguj się do Render

- Używając GitHub account (polecane)
- Lub Email

### Krok 3: Autoryzuj dostęp do repozytorium

Render poprosi o dostęp do repo GitHub - zaakceptuj

### Krok 4: Konfiguracja (już wszystko ustawione w render.yaml!)

Render automatycznie:
- Wykryje `render.yaml`
- Stworzy 2 serwisy (backend + frontend)
- Ustawi zmienne środowiskowe
- Rozpocznie deployment

### Krok 5: Czekaj na build (~5-10 minut)

Zobacz postęp w zakładce "Logs"

### Krok 6: Gotowe! 🎉

Po zakończeniu dostaniesz 2 URLe:
- **Backend API**: `https://movie-recommender-backend.onrender.com`
- **Frontend UI**: `https://movie-recommender-frontend.onrender.com`

---

## Metoda 2: Ręczny Deploy przez Dashboard

### Krok 1: Utwórz konto na Render.com

Wejdź na: https://dashboard.render.com/register

### Krok 2: Połącz GitHub

1. Dashboard → **Settings** → **Account**
2. Kliknij **Connect GitHub**
3. Autoryzuj Render

### Krok 3: Utwórz Backend Web Service

1. Dashboard → **New** → **Web Service**
2. Wybierz repozytorium: `PJATK-ASI-2024/ai_project_Michal_Czycza`
3. Wypełnij formularz:

```
Name: movie-recommender-backend
Environment: Docker
Branch: main
Region: Frankfurt (EU Central)
Dockerfile Path: ./app/Dockerfile
Docker Build Context: .
Plan: Free
```

4. **Advanced** → Environment Variables:
```
PORT = 8000
```

5. Kliknij **Create Web Service**

### Krok 4: Utwórz Frontend Web Service

1. Dashboard → **New** → **Web Service**
2. Wybierz to samo repozytorium
3. Wypełnij:

```
Name: movie-recommender-frontend
Environment: Docker
Branch: main
Region: Frankfurt (EU Central)
Dockerfile Path: ./frontend/Dockerfile
Docker Build Context: .
Plan: Free
```

4. **Advanced** → Environment Variables:
```
API_BASE_URL = https://movie-recommender-backend.onrender.com
PORT = 8501
```

5. Kliknij **Create Web Service**

### Krok 5: Czekaj na deploy

Każdy serwis będzie buildował się ~5-10 minut

---

## Poprawki dla Render

Render wymaga kilku zmian w Dockerfiles:

### 1. Backend Dockerfile musi używać portu z ENV

```dockerfile
# Dodaj na końcu app/Dockerfile
ENV PORT=8000
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2. Frontend musi używać portu 8501

Render automatycznie przekieruje ruch

---

## Verification - Sprawdzenie działania

Po deployu:

### Backend API
```bash
curl https://movie-recommender-backend.onrender.com/health
```

Oczekiwany wynik:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### API Documentation
```
https://movie-recommender-backend.onrender.com/docs
```

### Frontend UI
```
https://movie-recommender-frontend.onrender.com
```

---

## Troubleshooting

### Problem: Build timeout (15 min limit)

**Rozwiązanie**: 
1. Usuń zbędne zależności z requirements.txt
2. Użyj mniejszego base image
3. Upgrade do Starter plan ($7/miesiąc) - bez limitu czasu

### Problem: Out of memory podczas buildu

**Rozwiązanie**:
```dockerfile
# W Dockerfile dodaj:
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
```

### Problem: Free tier sleep po 15 min nieaktywności

**Informacja**: Darmowy tier śpi po 15 min braku ruchu, pierwsze uruchomienie trwa ~30s

**Rozwiązanie**: Upgrade do Starter ($7/miesiąc) dla always-on

### Problem: Frontend nie łączy się z backendem

**Sprawdź**:
1. Czy backend jest `Live` (zielony status)
2. Czy `API_BASE_URL` w frontend ma poprawny URL backendu
3. Czy backend ma włączone CORS (już jest w kodzie)

### Problem: 502 Bad Gateway

**Przyczyny**:
- Build się nie powiódł (sprawdź Logs)
- Port niepoprawnie skonfigurowany
- Healthcheck failuje

**Rozwiązanie**: Zobacz Logs w Dashboard

---

## Automatyczne Deploymenty

Po ustawieniu Render automatycznie deployuje przy każdym `git push`:

```bash
# Zmiany w kodzie
git add .
git commit -m "Update recommendation algorithm"
git push origin main

# Render automatycznie zdetekuje i zdeployuje!
```

---

## Monitorowanie

### Metrics
Dashboard → Service → **Metrics**
- CPU usage
- Memory usage
- Request count
- Response time

### Logs
Dashboard → Service → **Logs**
- Real-time logs
- Historical logs (7 days na free tier)

---

## Koszty

| Tier | Cena | Specyfikacja |
|------|------|--------------|
| **Free** | $0 | 512 MB RAM, śpi po 15 min, build limit 15 min |
| **Starter** | $7/miesiąc | 512 MB RAM, always-on, no build limit |
| **Standard** | $25/miesiąc | 2 GB RAM, always-on |

**Dla projektu studencki Free tier wystarczy!** ✅

---

## Publiczne URLe

Po deployu aplikacja będzie dostępna publicznie:

**Backend API:**
```
https://movie-recommender-backend.onrender.com
```

**API Docs (Swagger):**
```
https://movie-recommender-backend.onrender.com/docs
```

**Frontend:**
```
https://movie-recommender-frontend.onrender.com
```

**Możesz udostępnić te linki w dokumentacji projektu!** 🎉

---

## Custom Domain (Opcjonalnie)

Jeśli masz własną domenę:

1. Dashboard → Service → **Settings**
2. **Custom Domains** → **Add Custom Domain**
3. Dodaj rekord CNAME w DNS:
```
CNAME recommender.twojadomena.pl → movie-recommender-backend.onrender.com
```

---

## Dodatkowe Zasoby

- **Render Docs**: https://render.com/docs
- **Docker Support**: https://render.com/docs/docker
- **Status Page**: https://status.render.com/
- **Community Forum**: https://community.render.com/

---

## Następne Kroki

Po udanym wdrożeniu:

1. ✅ Dodaj linki do README.md
2. ✅ Zaktualizuj docs/docker_report.md z URL produkcyjnymi
3. ✅ Przetestuj wszystkie endpointy
4. ✅ Zrób screenshoty dla dokumentacji
5. ✅ Udostępnij link prowadzącemu (+10 punktów extra!)

---

**Deployment zakończony pomyślnie!** 🚀

Link do projektu: https://github.com/PJATK-ASI-2024/ai_project_Michal_Czycza
