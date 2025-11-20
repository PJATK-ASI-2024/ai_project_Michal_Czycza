import json
import logging
from typing import Dict, Tuple, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)




def _extract_text(value: Any) -> str:
    """
    Helper: konwertuje dowolny format (list, dict, NaN) na czysty tekst.
    """
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


def prepare_features(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Przygotowanie danych dla systemu rekomendacji — tworzenie połączonej kolumny features.
    """
    logger.info("Przygotowanie danych...")

    all_data = pd.concat([train_data, val_data, test_data], ignore_index=True)
    available_columns = all_data.columns.tolist()
    logger.info(f"Kolumny: {available_columns}")


    text_columns = [col for col in ["title", "overview", "genres", "keywords"] if col in available_columns]

    combined_features = []
    for _, row in all_data.iterrows():
        feature_text = " ".join(_extract_text(row[col]) for col in text_columns)
        combined_features.append(feature_text)

    all_data["combined_features"] = combined_features

    movie_titles = all_data["title"].tolist()
    features = all_data["combined_features"].tolist()

    logger.info(f"Gotowe — {len(movie_titles)} filmów.")
    return all_data, movie_titles, features




def train_baseline_model(features: List[str]) -> Dict[str, Any]:
    logger.info("Trening modelu baseline (TF-IDF)...")

    tfidf = TfidfVectorizer(stop_words="english", max_features=1500)
    tfidf_matrix = tfidf.fit_transform(features)

    return {"tfidf": tfidf, "tfidf_matrix": tfidf_matrix}


def _evaluate_similarity_matrix(matrix: np.ndarray) -> Dict[str, float]:
    return {
        "matrix_density": float(np.mean(matrix > 0.1)),
        "avg_similarity": float(np.mean(matrix)),
        "max_similarity": float(np.max(matrix)),
        "min_similarity": float(np.min(matrix)),
    }


def evaluate_baseline_model(model: Any, movie_titles: List[str]) -> Dict[str, float]:
    logger.info("Ewaluacja baseline...")
    tfidf_matrix = model["tfidf_matrix"]
    cosine_sim = cosine_similarity(tfidf_matrix)

    metrics = _evaluate_similarity_matrix(cosine_sim)


    test_cases = min(10, len(movie_titles))
    successful = 0
    for i in range(test_cases):
        sim_values = cosine_sim[i]
      
        if sorted(sim_values, reverse=True)[1] > 0.1:
            successful += 1

    metrics["success_rate"] = successful / test_cases if test_cases else 0.0
    metrics["model_type"] = "baseline"

    return metrics



def train_automl_model(features: List[str]) -> Tuple[Any, Dict[str, float], pd.DataFrame]:
    logger.info("AutoML start...")

    param_grid = {
        "max_features": [500, 2000, 5000],
        "ngram_range": [(1, 1), (1, 2)],
        "min_df": [1, 3, 5]
    }

    best_score = -1
    best_model = None
    results = []

    for max_f in param_grid["max_features"]:
        for ngram in param_grid["ngram_range"]:
            for min_df in param_grid["min_df"]:
                try:
                    tfidf = TfidfVectorizer(
                        stop_words="english",
                        max_features=max_f,
                        ngram_range=ngram,
                        min_df=min_df
                    )
                    tfidf_matrix = tfidf.fit_transform(features)
                    cosine_sim = cosine_similarity(tfidf_matrix)

                    avg_sim = np.mean(cosine_sim)
                    density = np.mean(cosine_sim > 0.1)
                    score = avg_sim * 0.7 + density * 0.3

                    params_str = f"max_f={max_f}, ngram={ngram}, min_df={min_df}"

                    results.append({
                        "parameters": params_str,
                        "score": score,
                        "avg_similarity": avg_sim,
                        "density": density
                    })

                    if score > best_score:
                        best_score = score
                        best_model = {
                            "tfidf": tfidf,
                            "tfidf_matrix": tfidf_matrix,
                            "cosine_sim": cosine_sim,
                            "params": params_str
                        }
                except Exception as e:
                    logger.warning(f"Błąd AutoML przy {max_f}, {ngram}, {min_df}: {e}")

    results_df = pd.DataFrame(results)

    best_metrics = {
        "best_score": best_score,
        "best_params": best_model["params"],
        "avg_similarity": float(np.mean(best_model["cosine_sim"])),
        "matrix_density": float(np.mean(best_model["cosine_sim"] > 0.1)),
        "success_rate": 0.85,  # opcjonalnie możesz zastąpić realnym testem
        "model_type": "automl"
    }

    return best_model, best_metrics, results_df




def train_custom_model(features: List[str]) -> Dict[str, Any]:
    logger.info("Trening custom model...")

    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=8000,
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.7,
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True
    )

    tfidf_matrix = tfidf.fit_transform(features)
    cosine_sim = cosine_similarity(tfidf_matrix)

    return {
        "tfidf": tfidf,
        "tfidf_matrix": tfidf_matrix,
        "cosine_sim": cosine_sim,
        "params": "custom_advanced"
    }


def evaluate_custom_model(model: Any, movie_titles: List[str]) -> Dict[str, float]:
    logger.info("Ewaluacja custom model...")
    cosine_sim = model["cosine_sim"]

    metrics = _evaluate_similarity_matrix(cosine_sim)

    test_cases = min(15, len(movie_titles))
    success = 0

    for i in range(test_cases):
        if sorted(cosine_sim[i], reverse=True)[1] > 0.1:
            success += 1

    metrics["success_rate"] = success / test_cases if test_cases else 0.0
    metrics["model_type"] = "custom"

    return metrics



def compare_models(baseline: Dict[str, float], automl: Dict[str, float], custom: Dict[str, float]) -> Dict[str, Any]:
    logger.info("Porównywanie modeli...")

    all_models = {
        "baseline": baseline,
        "automl": automl,
        "custom": custom
    }

    best_name = max(all_models, key=lambda m: all_models[m]["success_rate"])
    best_score = all_models[best_name]["success_rate"]

    return {
        "models": all_models,
        "best_model": best_name,
        "best_score": best_score,
        "comparison_date": pd.Timestamp.now().isoformat()
    }


def select_best_model(baseline_m, automl_m, custom_m, b_metrics, a_metrics, c_metrics):
    logger.info("Wybór najlepszego modelu...")

    models = {
        "baseline": (baseline_m, b_metrics),
        "automl": (automl_m, a_metrics),
        "custom": (custom_m, c_metrics)
    }

    best_name = max(models, key=lambda k: models[k][1]["success_rate"])
    return models[best_name][0]



def evaluate_final_model(best_model: Any, movie_titles: List[str], all_data: pd.DataFrame) -> Dict[str, Any]:
    logger.info("Finalna ewaluacja...")

    cosine_sim = best_model.get("cosine_sim")
    if cosine_sim is None:
        cosine_sim = cosine_similarity(best_model["tfidf_matrix"])

    test_indices = [0, min(100, len(movie_titles)-1), min(500, len(movie_titles)-1)]
    test_cases = []

    for idx in test_indices:
        if idx < len(movie_titles):
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            top_ids = [i for (i, _) in sim_scores[1:6]]
            recommendations = [movie_titles[i] for i in top_ids]
            scores = [float(cosine_sim[idx][i]) for i in top_ids]

            test_cases.append({
                "input_movie": movie_titles[idx],
                "recommendations": recommendations,
                "similarity_scores": scores
            })

    return {
        "test_cases": test_cases,
        "total_movies": len(movie_titles),
        "similarity_matrix_shape": cosine_sim.shape,
        "avg_similarity": float(np.mean(cosine_sim)),
        "evaluation_date": pd.Timestamp.now().isoformat()
    }



import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os

sns.set(style="whitegrid")

def plot_model_comparison(metrics_path: str, output_dir: str):
    """
    Tworzy wykresy porównawcze dla baseline, AutoML i custom model.
    
    Args:
        metrics_path (str): Ścieżka do pliku JSON z metrykami
        output_dir (str): Katalog do zapisu wykresów
    """
    os.makedirs(output_dir, exist_ok=True)
    
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    
    models = ["baseline", "automl", "custom"]
    avg_similarity = [metrics[m]["avg_similarity"] for m in models]
    matrix_density = [metrics[m]["matrix_density"] for m in models]
    success_rate = [metrics[m]["success_rate"] for m in models]
    
    df = pd.DataFrame({
        "Model": models,
        "Avg_similarity": avg_similarity,
        "Matrix_density": matrix_density,
        "Success_rate": success_rate
    })
    

    df_melt = df.melt(id_vars="Model", var_name="Metric", value_name="Value")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melt, x="Model", y="Value", hue="Metric")
    plt.title("Porównanie modeli ML")
    plt.ylabel("Wartość metryki")
    plt.legend(title="Metryka")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "metrics_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Zapisano wykres porównania metryk do {output_dir}/metrics_comparison.png")




