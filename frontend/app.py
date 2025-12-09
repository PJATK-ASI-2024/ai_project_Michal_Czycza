"""
Streamlit Frontend for Movie Recommender System
"""
import streamlit as st
import requests
import pandas as pd
from typing import List, Dict

API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Movie Recommender 🎬",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .movie-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #FF6B6B;
    }
    .movie-card h3 {
        color: #000000;
        font-weight: bold;
    }
    .similarity-score {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4ECDC4;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_recommendations(movie_title: str, top_n: int = 5):
    """Get movie recommendations from API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json={"movie_title": movie_title, "top_n": top_n},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, f"Movie '{movie_title}' not found. Try searching first."
        else:
            return None, f"Error: {response.json().get('detail', 'Unknown error')}"
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to API. Make sure backend is running on http://127.0.0.1:8000"
    except Exception as e:
        return None, f"Error: {str(e)}"

def search_movies(query: str):
    """Search for movies"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/search",
            params={"q": query, "limit": 10},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def main():
  
    st.markdown('<h1 class="main-header">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)
    st.markdown("### Find similar movies based on content similarity")
    
    
    with st.sidebar:
        st.header("⚙️ Settings")
       
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.warning("Start backend with: `uvicorn app.main:app --reload`")
        
        st.divider()
        
   
        top_n = st.slider(
            "Number of recommendations",
            min_value=1,
            max_value=20,
            value=5,
            help="How many similar movies to recommend"
        )
        
        st.divider()
        
        
        st.info("""
        **How it works:**
        1. Enter a movie title
        2. Click 'Get Recommendations'
        3. View similar movies ranked by similarity
        
        The system uses **TF-IDF** and **cosine similarity** 
        on movie metadata (title, overview, genres).
        """)
    

    col1, col2 = st.columns([2, 1])
    
    with col1:
        
        movie_title = st.text_input(
            "🎥 Enter a movie title:",
            placeholder="e.g., Avatar, Inception, The Matrix",
            help="Enter the title of a movie you like"
        )
    
    with col2:
        st.write("")  
        st.write("")  
        recommend_button = st.button("🔍 Get Recommendations", type="primary", use_container_width=True)
    

    if movie_title and len(movie_title) >= 3:
        with st.expander("💡 Search suggestions"):
            search_results = search_movies(movie_title)
            if search_results and search_results['count'] > 0:
                st.write(f"Found {search_results['count']} matches:")
                for movie in search_results['results']:
                    st.write(f"- **{movie['title']}** ({movie.get('release_date', 'N/A')[:4]})")
            else:
                st.write("No matches found. Try a different search term.")
    
 
    if recommend_button and movie_title:
        with st.spinner(f"Finding movies similar to '{movie_title}'..."):
            data, error = get_recommendations(movie_title, top_n)
            
            if error:
                st.error(error)
            elif data:
              
                st.success(f"✅ Found recommendations for: **{data['query_movie']}**")
                st.markdown(f"_Total movies in database: {data['total_movies_in_db']}_")
                
                st.divider()
                
                st.subheader("🎬 Recommended Movies")
                
                for i, movie in enumerate(data['recommendations'], 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="movie-card">
                            <h3>{i}. {movie['title']}</h3>
                            <p class="similarity-score">Similarity Score: {movie['similarity_score']:.2%}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            if movie.get('overview'):
                                st.write("**Overview:**", movie['overview'][:200] + "..." if len(movie.get('overview', '')) > 200 else movie.get('overview', 'N/A'))
                            if movie.get('genres'):
                                st.write("**Genres:**", movie['genres'][:100])
                        
                        with detail_col2:
                            if movie.get('vote_average'):
                                st.metric("⭐ Rating", f"{movie['vote_average']}/10")
                            if movie.get('release_date'):
                                st.write(f"📅 **Release:** {movie['release_date']}")
                        
                        st.divider()
    
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        Michal Czycza - AI Project Movies Recommender System 🎬
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
