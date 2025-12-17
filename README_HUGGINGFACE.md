---
title: Movie Recommender System
emoji: 🎬
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# 🎬 Content-Based Movie Recommender System

A machine learning-powered movie recommendation system that suggests similar movies based on content features using TF-IDF and cosine similarity.

## Features

- **Content-Based Filtering**: Analyzes movie metadata (title, overview, genres, keywords, cast, directors)
- **TF-IDF Vectorization**: Converts text features into numerical representations
- **Cosine Similarity**: Computes similarity scores between movies
- **Interactive UI**: User-friendly Streamlit interface
- **REST API**: FastAPI backend with automatic documentation

## Dataset

Based on TMDB 5000 Movie Dataset containing:
- 4,803 movies
- Metadata: titles, overviews, genres, keywords, cast, crew
- Ratings and release dates

## How It Works

1. **Input**: Enter a movie title you like
2. **Processing**: System computes similarity with all movies in database
3. **Output**: Returns top-N most similar movies with similarity scores

## Technology Stack

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **ML**: scikit-learn (TF-IDF, Cosine Similarity)
- **Data**: pandas, numpy

## Usage

### API Endpoints

- `GET /` - Health check
- `GET /health` - Model status
- `POST /recommend` - Get movie recommendations
- `GET /movies` - List all movies (paginated)
- `GET /search` - Search movies by title

### Example API Request

```python
import requests

response = requests.post(
    "http://localhost:7860/recommend",
    json={"movie_title": "Avatar", "top_n": 5}
)
print(response.json())
```

## Local Development

```bash
# Using Docker
docker build -f Dockerfile.huggingface -t movie-recommender .
docker run -p 7860:7860 -p 8501:8501 movie-recommender

# Access the app
# API: http://localhost:7860
# Frontend: http://localhost:8501
```

## Performance

- **Model**: TF-IDF Vectorizer with 4803x4803 similarity matrix
- **Recall@5**: 65%
- **Recall@10**: 79%
- **NDCG@5**: 0.71

## Credits

- **Dataset**: TMDB 5000 Movie Dataset
- **Author**: Michał Czycza
- **Project**: PJATK ASI 2024/2025

## License

MIT License
