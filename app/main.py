"""
FastAPI backend for Content-Based Movie Recommender System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import pickle
import pandas as pd
import numpy as np
from pathlib import Path


app = FastAPI(
    title="Movie Recommender API",
    description="Content-based movie recommendation system using TF-IDF and cosine similarity",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "data" / "reporting" / "best_model.pkl"
MOVIES_DATA_PATH = BASE_DIR / "data" / "raw" / "tmdb_5000_movies.csv"


model = None
movies_df = None
similarity_matrix = None

def load_model_and_data():
    """Load the trained model and movies dataset"""
    global model, movies_df, similarity_matrix
    
    try:
        
        with open(MODEL_PATH, "rb") as f:
            model_data = pickle.load(f)
            
        
        movies_df = pd.read_csv(MOVIES_DATA_PATH)
        
       
        if isinstance(model_data, dict):
            
            model = model_data.get('tfidf')
            tfidf_matrix = model_data.get('tfidf_matrix')
            
            if tfidf_matrix is not None:
              
                from sklearn.metrics.pairwise import cosine_similarity
                similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
            elif model is not None:
               
                movies_df['combined_features'] = (
                    movies_df['title'].fillna('') + ' ' +
                    movies_df['overview'].fillna('') + ' ' +
                    movies_df['genres'].fillna('')
                )
                tfidf_matrix = model.transform(movies_df['combined_features'])
                from sklearn.metrics.pairwise import cosine_similarity
                similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        else:
           
            model = model_data
            
        if model is None or movies_df is None:
            raise ValueError("Model or data not loaded properly")
            
        print("✅ Model and data loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False


@app.on_event("startup")
async def startup_event():
    success = load_model_and_data()
    if success:
        print("✅ Model and data loaded successfully")
    else:
        print("❌ Failed to load model and data")


class MovieRecommendationRequest(BaseModel):
    movie_title: str = Field(..., description="Title of the movie to get recommendations for")
    top_n: int = Field(default=5, ge=1, le=20, description="Number of recommendations to return")

class MovieInfo(BaseModel):
    title: str
    similarity_score: float
    overview: Optional[str]
    genres: Optional[str]
    vote_average: Optional[float]
    release_date: Optional[str]

class RecommendationResponse(BaseModel):
    query_movie: str
    recommendations: List[MovieInfo]
    total_movies_in_db: int


@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "message": "Movie Recommender API is running 🎬",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "recommendations": "/recommend",
            "movies_list": "/movies",
            "search": "/search"
        }
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "data_loaded": movies_df is not None,
        "total_movies": len(movies_df) if movies_df is not None else 0
    }

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: MovieRecommendationRequest):
    """
    Get movie recommendations based on a given movie title
    """
    if model is None or movies_df is None or similarity_matrix is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please try again later.")
    
    movie_title = request.movie_title.strip()
    top_n = request.top_n
    
 
    movie_matches = movies_df[
        movies_df['title'].str.contains(movie_title, case=False, na=False)
    ]
    
    if movie_matches.empty:
        raise HTTPException(
            status_code=404, 
            detail=f"Movie '{movie_title}' not found in database. Try /search?q={movie_title}"
        )
    
  
    movie_idx = movie_matches.index[0]
    matched_title = movie_matches.iloc[0]['title']
    

    similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
    

    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
 
    recommendations = []
    for idx, score in similarity_scores:
        movie = movies_df.iloc[idx]
        recommendations.append(MovieInfo(
            title=movie['title'],
            similarity_score=round(float(score), 4),
            overview=movie.get('overview'),
            genres=movie.get('genres'),
            vote_average=movie.get('vote_average'),
            release_date=movie.get('release_date')
        ))
    
    return RecommendationResponse(
        query_movie=matched_title,
        recommendations=recommendations,
        total_movies_in_db=len(movies_df)
    )

@app.get("/movies")
def list_movies(limit: int = 20, offset: int = 0, search: Optional[str] = None):
    """
    List all available movies in the database
    """
    if movies_df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    df = movies_df.copy()
    

    if search:
        df = df[df['title'].str.contains(search, case=False, na=False)]
    

    total = len(df)
    movies = df[['title', 'overview', 'genres', 'vote_average', 'release_date']].iloc[offset:offset+limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "movies": movies.to_dict(orient='records')
    }

@app.get("/search")
def search_movies(q: str, limit: int = 10):
    """
    Search for movies by title
    """
    if movies_df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    matches = movies_df[
        movies_df['title'].str.contains(q, case=False, na=False)
    ][['title', 'overview', 'vote_average', 'release_date']].head(limit)
    
    return {
        "query": q,
        "count": len(matches),
        "results": matches.to_dict(orient='records')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
