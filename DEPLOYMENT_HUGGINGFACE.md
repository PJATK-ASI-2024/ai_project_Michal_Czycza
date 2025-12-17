# 🚀 Deployment do HuggingFace Spaces - Instrukcja

## Krok 1: Utworzenie Space na HuggingFace

1. Wejdź na https://huggingface.co/spaces
2. Kliknij **"Create new Space"**
3. Wypełnij formularz:
   - **Space name**: `movie-recommender-system` (lub inna nazwa)
   - **License**: MIT
   - **Select SDK**: **Docker**
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public

4. Kliknij **"Create Space"**

## Krok 2: Przygotowanie Repozytorium Git

```powershell
# W katalogu projektu
cd C:\Users\micha\Desktop\ai_project_Michal_Czycza

# Inicjalizuj Git (jeśli jeszcze nie ma)
git init

# Dodaj remote do HuggingFace Space
git remote add space https://huggingface.co/spaces/mickelele03/movie-recommender-system

# Lub jeśli masz już inne remote:
git remote add hf https://huggingface.co/spaces/mickelele03/movie-recommender-system
```

## Krok 3: Przygotowanie Plików

Skopiuj lub zmień nazwę plików:

```powershell
# Skopiuj Dockerfile dla HuggingFace
Copy-Item Dockerfile.huggingface Dockerfile

# Skopiuj README
Copy-Item README_HUGGINGFACE.md README.md
```

## Krok 4: Commit i Push

```powershell
# Dodaj pliki do Git
git add Dockerfile
git add README.md
git add app/
git add frontend/
git add data/reporting/best_model.pkl
git add data/raw/tmdb_5000_movies.csv
git add requirements.txt

# Commit
git commit -m "Deploy movie recommender to HuggingFace Spaces"

# Push do HuggingFace (użyj tokena jako hasła)
git push space main
# lub
git push hf main

# Jeśli branch nazywa się master:
git push space master:main
```

## Krok 5: Uzyskanie Tokena HuggingFace

1. Wejdź na https://huggingface.co/settings/tokens
2. Kliknij **"New token"**
3. Wybierz **"Write"** access
4. Skopiuj token
5. Użyj jako hasła podczas `git push`

**Username**: Twoja nazwa użytkownika HuggingFace (mickelele03)  
**Password**: Wklej token

## Krok 6: Czekaj na Build

1. Wejdź na https://huggingface.co/spaces/mickelele03/movie-recommender-system
2. Space automatycznie zacznie budować się z Dockerfile
3. Zobacz logi budowania w zakładce **"Logs"**
4. Build potrwa ~10-15 minut

## Krok 7: Sprawdź Działanie

Po zakończeniu buildu Space będzie dostępny pod:
```
https://huggingface.co/spaces/mickelele03/movie-recommender-system
```

**Endpointy:**
- API Backend: `https://mickelele03-movie-recommender-system.hf.space/`
- API Docs: `https://mickelele03-movie-recommender-system.hf.space/docs`
- Frontend: `https://mickelele03-movie-recommender-system.hf.space:8501`

## Alternatywna Metoda: Bez Git (UI Upload)

1. Wejdź na swój Space
2. Kliknij **"Files"** → **"Add file"** → **"Upload files"**
3. Przeciągnij i upuść:
   - `Dockerfile` (zmień nazwę z Dockerfile.huggingface)
   - `README.md` (zmień nazwę z README_HUGGINGFACE.md)
   - Folder `app/`
   - Folder `frontend/`
   - Plik `data/reporting/best_model.pkl`
   - Plik `data/raw/tmdb_5000_movies.csv`
   - `requirements.txt`
4. Kliknij **"Commit changes"**

## Troubleshooting

### Problem: Build timeout
**Rozwiązanie**: Upgrade do paid tier (7€/miesiąc) dla więcej czasu budowania

### Problem: Out of memory
**Rozwiązanie**: 
- Zmniejsz rozmiar modelu
- Użyj CPU persistent hardware ($9/miesiąc)

### Problem: Port 8501 nie działa
**Rozwiązanie**: HuggingFace Spaces używa portu 7860 jako głównego. Zmień frontend na port 7860:
```dockerfile
CMD streamlit run frontend/app.py --server.port 7860
```

### Problem: Model nie ładuje się
**Rozwiązanie**: Sprawdź czy ścieżki w Dockerfile są poprawne i czy plik best_model.pkl jest w repozytorium

## Dodatkowe Opcje

### Streamlit Space (Prostsze, tylko frontend)

Jeśli chcesz tylko Streamlit bez osobnego backendu:

1. Wybierz SDK: **Streamlit** zamiast Docker
2. Wgraj tylko `frontend/app.py` jako `app.py`
3. Zintegruj model bezpośrednio w app.py (bez API calls)

### Render.com (Alternatywa)

1. Wejdź na https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Render automatycznie wykryje Dockerfile
5. Deploy

## Linki

- **HuggingFace Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Docker SDK Guide**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Your Space**: https://huggingface.co/spaces/mickelele03/movie-recommender-system

---

**Potrzebujesz pomocy?** 
- Discord: https://discord.gg/hugging-face
- Forum: https://discuss.huggingface.co/
