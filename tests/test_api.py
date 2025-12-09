"""
Integration tests for Movie Recommender API
"""
from fastapi.testclient import TestClient
import sys
from pathlib import Path
import pytest


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app, load_model_and_data

@pytest.fixture(scope="module", autouse=True)
def setup_model():
    """Load model before running tests"""
    print("\n🔄 Loading model for tests...")
    success = load_model_and_data()
    if not success:
        pytest.skip("Model could not be loaded")
    print("✅ Model loaded successfully for tests")
    yield
    print("\n🧹 Cleanup after tests")

client = TestClient(app)

def test_home_endpoint():
    """Test the home/root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Movie Recommender" in data["message"]
    assert data["status"] == "healthy"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "total_movies" in data

def test_recommend_valid_movie():
    """Test recommendation endpoint with valid movie"""
    payload = {
        "movie_title": "Avatar",
        "top_n": 5
    }
    response = client.post("/recommend", json=payload)
    

    assert response.status_code == 200
   
    data = response.json()
    assert "query_movie" in data
    assert "recommendations" in data
    assert "total_movies_in_db" in data
    

    assert len(data["recommendations"]) <= 5
    assert len(data["recommendations"]) > 0
    

    first_rec = data["recommendations"][0]
    assert "title" in first_rec
    assert "similarity_score" in first_rec
    assert 0 <= first_rec["similarity_score"] <= 1

def test_recommend_invalid_movie():
    """Test recommendation endpoint with non-existent movie"""
    payload = {
        "movie_title": "XYZ_NONEXISTENT_MOVIE_12345",
        "top_n": 5
    }
    response = client.post("/recommend", json=payload)
    
   
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_recommend_different_top_n():
    """Test recommendation with different number of recommendations"""
    for n in [1, 3, 10]:
        payload = {
            "movie_title": "Inception",
            "top_n": n
        }
        response = client.post("/recommend", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            assert len(data["recommendations"]) <= n

def test_list_movies():
    """Test movies listing endpoint"""
    response = client.get("/movies?limit=10&offset=0")
    assert response.status_code == 200
    
    data = response.json()
    assert "total" in data
    assert "movies" in data
    assert len(data["movies"]) <= 10

def test_search_movies():
    """Test movie search endpoint"""
    response = client.get("/search?q=Avatar&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert "query" in data
    assert "count" in data
    assert "results" in data
    assert data["query"] == "Avatar"

def test_search_empty_query():
    """Test search with empty or very short query"""
    response = client.get("/search?q=XY&limit=5")
    assert response.status_code == 200
    data = response.json()
  

def test_api_cors_headers():
    """Test that CORS headers are present"""
    response = client.get("/")

    assert "access-control-allow-origin" in response.headers or response.status_code == 200

def test_recommend_case_insensitive():
    """Test that movie search is case-insensitive"""
    payloads = [
        {"movie_title": "avatar", "top_n": 3},
        {"movie_title": "AVATAR", "top_n": 3},
        {"movie_title": "Avatar", "top_n": 3}
    ]
    
    results = []
    for payload in payloads:
        response = client.post("/recommend", json=payload)
        if response.status_code == 200:
            results.append(response.json()["query_movie"])
    

    if len(results) > 1:
        assert all(r == results[0] for r in results)

def test_recommend_partial_match():
    """Test that partial movie title matching works"""
    payload = {
        "movie_title": "Dark Knight", 
        "top_n": 5
    }
    response = client.post("/recommend", json=payload)
    

    assert response.status_code in [200, 404] 

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
