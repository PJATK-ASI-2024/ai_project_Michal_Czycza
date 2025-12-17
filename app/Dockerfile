# Etap 1 — obraz bazowy
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj requirements.txt
COPY requirements.txt /app/requirements.txt

# Instalacja zależności (tylko te potrzebne dla backendu)
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    pydantic==2.6.0 \
    python-multipart==0.0.6 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    scikit-learn==1.3.0 \
    requests==2.31.0

# Skopiuj kod aplikacji
COPY ./app /app

# Skopiuj dane (model i dataset)
COPY ./data/reporting/best_model.pkl /app/data/reporting/best_model.pkl
COPY ./data/raw/tmdb_5000_movies.csv /app/data/raw/tmdb_5000_movies.csv

# Port API
EXPOSE 8000
ENV PORT=8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Komenda startowa (Render używa zmiennej PORT)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
