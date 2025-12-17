# Dockerfile dla frontendu Streamlit
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /frontend

# Skopiuj wymagania
COPY requirements.txt /frontend/requirements.txt

# Instalacja zależności dla frontendu
RUN pip install --no-cache-dir \
    streamlit==1.31.0 \
    requests==2.31.0 \
    pandas==2.0.3

# Skopiuj kod frontendu
COPY ./frontend /frontend

# Port Streamlit
EXPOSE 8501
ENV PORT=8501

# Healthcheck dla Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Komenda startowa (Render używa zmiennej PORT)
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true
