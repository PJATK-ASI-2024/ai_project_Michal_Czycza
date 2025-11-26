import logging
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import KFold
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def _extract_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    
    if isinstance(value, list):
        result = []
        for item in value:
            if isinstance(item, dict) and "name" in item:
                result.append(str(item["name"]))
            else:
                result.append(str(item))
        return " ".join(result)
    
    if isinstance(value, dict):
        return " ".join(str(v) for v in value.values())
    
    return str(value)


def cross_validate_baseline_model(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    test_data: pd.DataFrame,
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    Walidacja krzyżowa dla modelu baseline.
    Łączy train/val/test, przeprowadza K-fold cross-validation.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    logger.info(f"Cross-validation (K={n_splits}) dla baseline model...")
    

    all_data = pd.concat([train_data, val_data, test_data], ignore_index=True).reset_index(drop=True)
    available_columns = all_data.columns.tolist()
    text_columns = [col for col in ["title", "overview", "genres", "keywords"] if col in available_columns]
    

    combined_features = []
    for _, row in all_data.iterrows():
        feature_text = " ".join(_extract_text(row[col]) for col in text_columns)
        combined_features.append(feature_text)
    
    all_data["combined_features"] = combined_features
    features = all_data["combined_features"].tolist()
    
 
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_metrics = []
    
    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(features)):
        logger.info(f"  Fold {fold_idx + 1}/{n_splits}")
        
        train_features = [features[i] for i in train_idx]
        val_features = [features[i] for i in val_idx]
        
    
        tfidf = TfidfVectorizer(stop_words="english", max_features=1500)
        tfidf_matrix_train = tfidf.fit_transform(train_features)
        tfidf_matrix_val = tfidf.transform(val_features)
        
      
        cosine_sim_val = cosine_similarity(tfidf_matrix_val, tfidf_matrix_train)
        
      
        fold_metric = _compute_recommendation_metrics(cosine_sim_val, k_values=[5, 10, 20])
        fold_metrics.append(fold_metric)
    
   
    avg_metrics = {
        "recall_5": np.mean([m["recall_5"] for m in fold_metrics]),
        "recall_10": np.mean([m["recall_10"] for m in fold_metrics]),
        "recall_20": np.mean([m["recall_20"] for m in fold_metrics]),
        "ndcg_5": np.mean([m["ndcg_5"] for m in fold_metrics]),
        "ndcg_10": np.mean([m["ndcg_10"] for m in fold_metrics]),
        "map_5": np.mean([m["map_5"] for m in fold_metrics]),
        "map_10": np.mean([m["map_10"] for m in fold_metrics]),
        "avg_similarity": np.mean([m["avg_similarity"] for m in fold_metrics]),
        "std_similarity": np.std([m["avg_similarity"] for m in fold_metrics]),
    }
    
    logger.info(f"Cross-validation completed. Recall@5: {avg_metrics['recall_5']:.4f}")
    
    return {
        "fold_metrics": fold_metrics,
        "averaged_metrics": avg_metrics,
        "n_splits": n_splits,
        "total_samples": len(features)
    }


def _compute_recommendation_metrics(
    similarity_matrix: np.ndarray,
    k_values: List[int] = [5, 10, 20]
) -> Dict[str, float]:
    """
    Oblicza metryki dla systemu rekomendacji:
    - Recall@K: proporcja relewantnych elementów w top-K
    - NDCG@K: Normalized Discounted Cumulative Gain
    - MAP@K: Mean Average Precision
    """
    n_test_samples = similarity_matrix.shape[0]
    
    recalls = {}
    ndcgs = {}
    maps = {}
    
    for k in k_values:
        if k > similarity_matrix.shape[1]:
            k = similarity_matrix.shape[1]
        

        recall_k = 0
        ndcg_k = 0
        map_k = 0
        
        for i in range(n_test_samples):
            sim_scores = similarity_matrix[i]
            top_k_indices = np.argsort(-sim_scores)[:k]
            top_k_similarities = sim_scores[top_k_indices]
            
           
            relevant = np.sum(top_k_similarities > 0.3)
            recall_k += relevant / k if k > 0 else 0
            
          
            idcg = np.sum(1.0 / np.log2(np.arange(2, min(k + 2, len(top_k_similarities) + 2))))
            dcg = np.sum(
                (top_k_similarities > 0.3).astype(float) / np.log2(np.arange(2, k + 2))
            )
            ndcg_k += dcg / idcg if idcg > 0 else 0
            
           
            precisions = []
            for j in range(k):
                if top_k_similarities[j] > 0.3:
                    precisions.append((len(precisions) + 1) / (j + 1))
            map_k += np.mean(precisions) if precisions else 0
        
        recalls[f"recall_{k}"] = recall_k / n_test_samples
        ndcgs[f"ndcg_{k}"] = ndcg_k / n_test_samples
        maps[f"map_{k}"] = map_k / n_test_samples
    
    return {
        **recalls,
        **ndcgs,
        **maps,
        "avg_similarity": float(np.mean(similarity_matrix)),
        "max_similarity": float(np.max(similarity_matrix)),
        "min_similarity": float(np.min(similarity_matrix))
    }


def evaluate_baseline_on_test_set(
    baseline_model: Dict[str, Any],
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> Dict[str, Any]:
    """
    Finalna ewaluacja baseline modelu na test set.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    logger.info("Ewaluacja baseline na test set...")

    train_all = pd.concat([train_data, val_data], ignore_index=True).reset_index(drop=True)
    available_columns = test_data.columns.tolist()
    text_columns = [col for col in ["title", "overview", "genres", "keywords"] if col in available_columns]
    

    train_features = []
    for _, row in train_all.iterrows():
        feature_text = " ".join(_extract_text(row[col]) for col in text_columns)
        train_features.append(feature_text)
 
    test_features = []
    for _, row in test_data.iterrows():
        feature_text = " ".join(_extract_text(row[col]) for col in text_columns)
        test_features.append(feature_text)
    

    tfidf = TfidfVectorizer(stop_words="english", max_features=1500)
    tfidf_matrix_train = tfidf.fit_transform(train_features)
    tfidf_matrix_test = tfidf.transform(test_features)
    
  
    cosine_sim = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    

    metrics = _compute_recommendation_metrics(cosine_sim, k_values=[5, 10, 20])
    

    test_cases = []
    for i in range(min(5, len(test_data))):
        sim_scores = list(enumerate(cosine_sim[i]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        top_indices = [idx for (idx, _) in sim_scores[1:6]]
        recommendations = [train_all.iloc[idx]["title"] if "title" in train_all.columns else f"Movie_{idx}" 
                          for idx in top_indices]
        scores = [float(cosine_sim[i][idx]) for idx in top_indices]
        
        test_cases.append({
            "query_movie": test_data.iloc[i]["title"] if "title" in test_data.columns else f"Test_Movie_{i}",
            "recommendations": recommendations,
            "similarity_scores": scores
        })
    
    return {
        "test_metrics": metrics,
        "test_cases": test_cases,
        "test_set_size": len(test_data),
        "train_set_size": len(train_all),
        "evaluation_timestamp": datetime.now().isoformat()
    }


def compute_feature_importance(
    baseline_model: Dict[str, Any],
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> Dict[str, Any]:
    """
    Analiza ważności cech na podstawie TF-IDF wag.
    """
    logger.info("Obliczanie ważności cech...")
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    

    all_data = pd.concat([train_data, val_data, test_data], ignore_index=True).reset_index(drop=True)
    available_columns = all_data.columns.tolist()
    text_columns = [col for col in ["title", "overview", "genres", "keywords"] if col in available_columns]
    

    combined_features = []
    for _, row in all_data.iterrows():
        feature_text = " ".join(_extract_text(row[col]) for col in text_columns)
        combined_features.append(feature_text)
    

    tfidf = TfidfVectorizer(stop_words="english", max_features=1500)
    tfidf_matrix = tfidf.fit_transform(combined_features)
    

    mean_weights = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    feature_names = tfidf.get_feature_names_out()
    
    
    top_indices = np.argsort(-mean_weights)[:20]
    top_features = [(feature_names[i], float(mean_weights[i])) for i in top_indices]
    
    logger.info(f"Top features: {[f[0] for f in top_features[:5]]}")
    
    return {
        "top_features": top_features,
        "feature_count": len(feature_names),
        "total_features_vocabulary": len(feature_names),
        "mean_tfidf_weight": float(np.mean(mean_weights)),
        "std_tfidf_weight": float(np.std(mean_weights))
    }


def generate_model_version_record(
    cv_results: Dict[str, Any],
    test_results: Dict[str, Any],
    feature_importance: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Tworzenie rekordu wersji modelu z wszystkimi metrykami.
    """
    logger.info("Generowanie rekordu wersji modelu...")
    
    timestamp = datetime.now().isoformat()
    version = f"baseline_v1.0"
    
    record = {
        "timestamp": timestamp,
        "version": version,
        "model_name": "baseline_tfidf_cosine_similarity",
        "model_type": "content_based_recommender",
        
      
        "cv_recall_5": cv_results["averaged_metrics"]["recall_5"],
        "cv_recall_10": cv_results["averaged_metrics"]["recall_10"],
        "cv_recall_20": cv_results["averaged_metrics"]["recall_20"],
        "cv_ndcg_5": cv_results["averaged_metrics"]["ndcg_5"],
        "cv_ndcg_10": cv_results["averaged_metrics"]["ndcg_10"],
        "cv_map_5": cv_results["averaged_metrics"]["map_5"],
        "cv_map_10": cv_results["averaged_metrics"]["map_10"],
        "cv_avg_similarity": cv_results["averaged_metrics"]["avg_similarity"],
        
       
        "test_recall_5": test_results["test_metrics"]["recall_5"],
        "test_recall_10": test_results["test_metrics"]["recall_10"],
        "test_recall_20": test_results["test_metrics"]["recall_20"],
        "test_ndcg_5": test_results["test_metrics"]["ndcg_5"],
        "test_ndcg_10": test_results["test_metrics"]["ndcg_10"],
        "test_map_5": test_results["test_metrics"]["map_5"],
        "test_map_10": test_results["test_metrics"]["map_10"],
        "test_avg_similarity": test_results["test_metrics"]["avg_similarity"],
        
        
        "train_set_size": test_results["train_set_size"],
        "test_set_size": test_results["test_set_size"],
        "total_vocabulary": feature_importance["total_features_vocabulary"],
        "top_feature_1": feature_importance["top_features"][0][0],
        "top_feature_2": feature_importance["top_features"][1][0],
        "top_feature_3": feature_importance["top_features"][2][0],
    }
    
    logger.info(f"Model version record created: {version}")
    return record


def save_model_version_csv(
    model_version_record: Dict[str, Any],
    csv_path: str = "data/reporting/model_versions.csv"
) -> None:
    """
    Zapisuje rekord wersji modelu do CSV.
    """
    logger.info(f"Saving model version to {csv_path}...")
    
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
   
    df_new = pd.DataFrame([model_version_record])
    
 
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    df_combined.to_csv(csv_path, index=False)
    logger.info(f"Model version saved to {csv_path}")


def log_to_mlflow(
    cv_results: Dict[str, Any],
    test_results: Dict[str, Any],
    feature_importance: Dict[str, Any]
) -> None:
    """
    Logging metryk do MLflow.
    """
    try:
        import mlflow
        
        logger.info("Logging to MLflow...")
        
        with mlflow.start_run():

            mlflow.log_param("model_type", "baseline_tfidf_cosine_similarity")
            mlflow.log_param("tfidf_max_features", 1500)
            mlflow.log_param("tfidf_stop_words", "english")
            

            mlflow.log_metric("cv_recall_5", cv_results["averaged_metrics"]["recall_5"])
            mlflow.log_metric("cv_recall_10", cv_results["averaged_metrics"]["recall_10"])
            mlflow.log_metric("cv_ndcg_5", cv_results["averaged_metrics"]["ndcg_5"])
            mlflow.log_metric("cv_ndcg_10", cv_results["averaged_metrics"]["ndcg_10"])
            mlflow.log_metric("cv_map_5", cv_results["averaged_metrics"]["map_5"])
            mlflow.log_metric("cv_map_10", cv_results["averaged_metrics"]["map_10"])
            mlflow.log_metric("cv_avg_similarity", cv_results["averaged_metrics"]["avg_similarity"])
            

            mlflow.log_metric("test_recall_5", test_results["test_metrics"]["recall_5"])
            mlflow.log_metric("test_recall_10", test_results["test_metrics"]["recall_10"])
            mlflow.log_metric("test_ndcg_5", test_results["test_metrics"]["ndcg_5"])
            mlflow.log_metric("test_ndcg_10", test_results["test_metrics"]["ndcg_10"])
            mlflow.log_metric("test_map_5", test_results["test_metrics"]["map_5"])
            mlflow.log_metric("test_map_10", test_results["test_metrics"]["map_10"])
            mlflow.log_metric("test_avg_similarity", test_results["test_metrics"]["avg_similarity"])
            
           
            mlflow.log_param("top_feature_1", feature_importance["top_features"][0][0])
            mlflow.log_param("top_feature_2", feature_importance["top_features"][1][0])
            
            logger.info("MLflow logging completed")
    
    except ImportError:
        logger.warning("MLflow not installed. Skipping MLflow logging.")
    except Exception as e:
        logger.warning(f"MLflow logging failed: {e}")
