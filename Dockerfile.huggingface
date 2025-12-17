# Multi-stage Dockerfile for HuggingFace Spaces
# Combines backend and frontend in one container

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    pydantic==2.6.0 \
    python-multipart==0.0.6 \
    streamlit==1.31.0 \
    requests==2.31.0 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    scikit-learn==1.3.0

# Copy application code
COPY ./app /app/backend
COPY ./frontend /app/frontend

# Copy data files
COPY ./data/reporting/best_model.pkl /app/backend/data/reporting/best_model.pkl
COPY ./data/raw/tmdb_5000_movies.csv /app/backend/data/raw/tmdb_5000_movies.csv

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 7860 &\n\
sleep 5\n\
cd /app/frontend && streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports (HuggingFace uses 7860)
EXPOSE 7860
EXPOSE 8501

# Run startup script
CMD ["/bin/bash", "/app/start.sh"]
