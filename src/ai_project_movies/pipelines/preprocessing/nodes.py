import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import ast

def merge_datasets(movies_df, credits_df):
    print("Kolumny w movies_df:", movies_df.columns.tolist())
    print("Kolumny w credits_df:", credits_df.columns.tolist())
    
    merged_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')
    
    if 'title_x' in merged_df.columns and 'title_y' in merged_df.columns:
        merged_df = merged_df.rename(columns={'title_x': 'title'})
        merged_df = merged_df.drop(columns=['title_y'])
        print("Rozwiązano konflikt kolumn title - użyto title_x")
    
    text_columns = ['genres', 'keywords', 'cast', 'crew']
    
    for col in text_columns:
        if col in merged_df.columns:
            try:
                if col == 'genres':
                    merged_df[col] = merged_df[col].apply(lambda x: [i['name'] for i in ast.literal_eval(x)] if pd.notna(x) else [])
                elif col == 'keywords':
                    merged_df[col] = merged_df[col].apply(lambda x: [i['name'] for i in ast.literal_eval(x)] if pd.notna(x) else [])
                elif col == 'cast':
                    merged_df[col] = merged_df[col].apply(lambda x: [i['name'] for i in ast.literal_eval(x)[:5]] if pd.notna(x) else [])
                elif col == 'crew':
                    merged_df[col] = merged_df[col].apply(lambda x: [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director'] if pd.notna(x) else [])
            except (ValueError, SyntaxError):
                merged_df[col] = merged_df[col].apply(lambda x: [] if pd.notna(x) else [])

    def create_combined_features(row):
        features = []
        
        if pd.notna(row.get('title')):
            features.append(str(row['title']))
        elif pd.notna(row.get('original_title')):
            features.append(str(row['original_title']))
            
        if pd.notna(row.get('overview')):
            features.append(str(row['overview']))
            
        if 'genres' in row and isinstance(row['genres'], list):
            features.append(" ".join([str(g) for g in row['genres']]))
            
        if 'keywords' in row and isinstance(row['keywords'], list):
            features.append(" ".join([str(k) for k in row['keywords']]))
            
        return " ".join(features)
    
    merged_df["combined_features"] = merged_df.apply(create_combined_features, axis=1)
    
    print(f"Połączono dataset. Rozmiar: {merged_df.shape}")
    print("Kolumny po mergowaniu:", merged_df.columns.tolist())
    print(f"Przykładowe combined_features: {merged_df['combined_features'].iloc[0][:100]}...")
    
    return merged_df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Kolumny przed czyszczeniem:", df.columns.tolist())
    
    if 'title' not in df.columns:
        if 'title_x' in df.columns:
            df = df.rename(columns={'title_x': 'title'})
            print("Przemianowano title_x na title")
        elif 'original_title' in df.columns:
            df = df.rename(columns={'original_title': 'title'})
            print("Przemianowano original_title na title")
        else:
            df['title'] = ""
            print("Utworzono pustą kolumnę title")
    
    if 'overview' not in df.columns:
        df['overview'] = ""
        print("Utworzono pustą kolumnę overview")
    
    df = df.drop_duplicates(subset="id")
    print(f"Po usunięciu duplikatów: {df.shape}")
    
    df = df.dropna(subset=["title", "overview"])
    print(f"Po usunięciu brakujących title/overview: {df.shape}")
    

    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
    

    if 'popularity' in df.columns:
        df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce").fillna(0)
    
    if 'vote_average' in df.columns:
        df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce").fillna(0)
    
    if 'vote_count' in df.columns:
        df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce").fillna(0)
    

    text_cols = df.select_dtypes(include=[object]).columns
    for col in text_cols:
        if col not in ['title', 'overview', 'combined_features']:
            df[col] = df[col].fillna("")
    
    print(f"Po czyszczeniu. Ostateczny rozmiar: {df.shape}")
    return df

def scale_data(df: pd.DataFrame) -> pd.DataFrame:
    """Skaluje cechy numeryczne."""
    
    print("Skalowanie danych...")
    
    num_cols = ["popularity", "vote_average", "vote_count"]
    available_num_cols = [col for col in num_cols if col in df.columns]
    
    if available_num_cols:
        scaler = StandardScaler()
        df_scaled = df.copy()
        df_scaled[available_num_cols] = scaler.fit_transform(df[available_num_cols])
        print(f"Przeskalowano kolumny: {available_num_cols}")
    else:
        df_scaled = df.copy()
        print("Brak kolumn numerycznych do skalowania")
    
    return df_scaled

def split_data(df: pd.DataFrame):
    print("Dzielenie danych...")
    
    if len(df) < 10:
        raise ValueError("Za mało danych do podziału")
    
    train, temp = train_test_split(df, test_size=0.3, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)
    
    print(f"Podział danych: train={len(train)}, val={len(val)}, test={len(test)}")
    
    return train, val, test