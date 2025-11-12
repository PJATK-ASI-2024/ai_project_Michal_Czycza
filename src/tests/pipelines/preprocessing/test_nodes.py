import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from src.ai_project_movies.pipelines.preprocessing.nodes import (
    merge_datasets, clean_data, scale_data, split_data
)


class TestPreprocessingNodes:
    
    def test_merge_datasets(self):
        """Test łączenia datasetów."""

        movies_data = {
            'id': [1, 2, 3],
            'title': ['Movie 1', 'Movie 2', 'Movie 3'],
            'overview': ['Overview 1', 'Overview 2', 'Overview 3'],
            'genres': ['[{"id": 1, "name": "Action"}]', '[{"id": 2, "name": "Drama"}]', '[{"id": 3, "name": "Comedy"}]'],
            'popularity': [100, 200, 300],
            'vote_average': [7.5, 8.0, 6.5],
            'vote_count': [1000, 2000, 3000]
        }
        
        credits_data = {
            'movie_id': [1, 2, 3],
            'cast': ['[{"name": "Actor 1"}]', '[{"name": "Actor 2"}]', '[{"name": "Actor 3"}]'],
            'crew': ['[{"job": "Director", "name": "Director 1"}]', '[{"job": "Director", "name": "Director 2"}]', '[{"job": "Producer", "name": "Producer 1"}]']
        }
        
        movies_df = pd.DataFrame(movies_data)
        credits_df = pd.DataFrame(credits_data)
        

        result = merge_datasets(movies_df, credits_df)
        

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'combined_features' in result.columns
        assert 'title' in result.columns
        assert 'genres' in result.columns
        assert isinstance(result['genres'].iloc[0], list)
        assert result['genres'].iloc[0] == ['Action']

    def test_clean_data(self):
        """Test czyszczenia danych."""

        test_data = {
            'id': [1, 2, 3, 4],
            'title': ['Movie 1', 'Movie 2', None, 'Movie 4'],
            'overview': ['Overview 1', None, 'Overview 3', 'Overview 4'],
            'popularity': [100, 200, None, 400],
            'vote_average': [7.5, None, 6.5, 8.0],
            'vote_count': [1000, 2000, 3000, None]
        }
        
        df = pd.DataFrame(test_data)
        

        result = clean_data(df)
        

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0  
        assert result['popularity'].isna().sum() == 0
        assert result['vote_average'].isna().sum() == 0
        assert result['vote_count'].isna().sum() == 0
        assert result['title'].isna().sum() == 0
        assert result['overview'].isna().sum() == 0

    def test_clean_data_duplicates(self):
        """Test usuwania duplikatów."""
        test_data = {
            'id': [1, 1, 2, 3], 
            'title': ['Movie 1', 'Movie 1', 'Movie 2', 'Movie 3'],
            'overview': ['Overview 1', 'Overview 1', 'Overview 2', 'Overview 3'],
            'popularity': [100, 100, 200, 300],
            'vote_average': [7.5, 7.5, 8.0, 6.5], 
            'vote_count': [1000, 1000, 2000, 3000]
        }
        
        df = pd.DataFrame(test_data)
        result = clean_data(df)
        

        assert len(result) == 3
        assert result['id'].nunique() == 3

    def test_clean_data_missing_columns(self):
        """Test czyszczenia danych z brakującymi kolumnami."""
        test_data = {
            'id': [1, 2, 3],
            'title': ['Movie 1', 'Movie 2', 'Movie 3'],
            'overview': ['Overview 1', 'Overview 2', 'Overview 3'],
            'popularity': [100, 200, 300]

        }
        
        df = pd.DataFrame(test_data)
        result = clean_data(df)
        

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'title' in result.columns
        assert 'overview' in result.columns

    def test_scale_data(self):
        """Test skalowania danych."""
        test_data = {
            'id': [1, 2, 3],
            'title': ['Movie 1', 'Movie 2', 'Movie 3'],
            'popularity': [100, 200, 300],
            'vote_average': [7.5, 8.0, 6.5],
            'vote_count': [1000, 2000, 3000]
        }
        
        df = pd.DataFrame(test_data)
        result = scale_data(df)
        
        assert isinstance(result, pd.DataFrame)
        assert 'popularity' in result.columns
        assert 'vote_average' in result.columns
        assert 'vote_count' in result.columns
        
        scaler = StandardScaler()
        expected_scaled = scaler.fit_transform(df[['popularity', 'vote_average', 'vote_count']])
        
        np.testing.assert_array_almost_equal(
            result[['popularity', 'vote_average', 'vote_count']].values,
            expected_scaled,
            decimal=5
        )

    def test_scale_data_missing_columns(self):
        """Test skalowania danych z brakującymi kolumnami."""
        test_data = {
            'id': [1, 2, 3],
            'title': ['Movie 1', 'Movie 2', 'Movie 3'],
            'popularity': [100, 200, 300]
        }
        
        df = pd.DataFrame(test_data)
        result = scale_data(df)
        
        assert isinstance(result, pd.DataFrame)
        assert 'popularity' in result.columns

    def test_split_data(self):
        """Test podziału danych."""
        test_data = {
            'id': range(100),
            'title': [f'Movie {i}' for i in range(100)],
            'overview': [f'Overview {i}' for i in range(100)],
            'popularity': np.random.normal(100, 50, 100),
            'vote_average': np.random.normal(7, 1, 100)
        }
        
        df = pd.DataFrame(test_data)
        train, val, test = split_data(df)
        
        # Asercje
        assert isinstance(train, pd.DataFrame)
        assert isinstance(val, pd.DataFrame)
        assert isinstance(test, pd.DataFrame)
        
        total_len = len(train) + len(val) + len(test)
        assert total_len == len(df)
        assert len(train) / total_len == pytest.approx(0.7, abs=0.05)  # 70% ±5%
        assert len(val) / total_len == pytest.approx(0.15, abs=0.05)   # 15% ±5%
        assert len(test) / total_len == pytest.approx(0.15, abs=0.05)  # 15% ±5%
        
        train_ids = set(train['id'])
        val_ids = set(val['id'])
        test_ids = set(test['id'])
        
        assert train_ids.isdisjoint(val_ids)
        assert train_ids.isdisjoint(test_ids)
        assert val_ids.isdisjoint(test_ids)

    def test_split_data_small_dataset(self):
        """Test podziału małego datasetu."""
        test_data = {
            'id': [1, 2],
            'title': ['Movie 1', 'Movie 2'],
            'overview': ['Overview 1', 'Overview 2'],
            'popularity': [100, 200]
        }
        
        df = pd.DataFrame(test_data)
        
        with pytest.raises(ValueError, match="Za mało danych do podziału"):
            split_data(df)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])