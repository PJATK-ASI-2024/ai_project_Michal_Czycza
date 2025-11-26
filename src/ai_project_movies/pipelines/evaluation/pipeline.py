from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    cross_validate_baseline_model,
    evaluate_baseline_on_test_set,
    compute_feature_importance,
    generate_model_version_record,
    save_model_version_csv,
    log_to_mlflow,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Pipeline do ewaluacji i wersjonowania baseline modelu.
    
    Kroki:
    1. Cross-validation na train/val/test
    2. Ewaluacja na test set
    3. Obliczanie feature importance
    4. Generowanie rekordu wersji
    5. Zapis do CSV i MLflow
    """
    return pipeline(
        [
            node(
                func=cross_validate_baseline_model,
                inputs=["train_data", "val_data", "test_data"],
                outputs="cv_results",
                name="cross_validate_baseline_node",
            ),
            
            node(
                func=evaluate_baseline_on_test_set,
                inputs=["baseline_model", "train_data", "val_data", "test_data"],
                outputs="test_evaluation_results",
                name="evaluate_baseline_test_node",
            ),
            
            node(
                func=compute_feature_importance,
                inputs=["baseline_model", "train_data", "val_data", "test_data"],
                outputs="feature_importance_results",
                name="compute_feature_importance_node",
            ),
            
            node(
                func=generate_model_version_record,
                inputs=["cv_results", "test_evaluation_results", "feature_importance_results"],
                outputs="model_version_record",
                name="generate_model_version_record_node",
            ),
            
            node(
                func=save_model_version_csv,
                inputs="model_version_record",
                outputs=None,
                name="save_model_version_csv_node",
            ),
            
            node(
                func=log_to_mlflow,
                inputs=["cv_results", "test_evaluation_results", "feature_importance_results"],
                outputs=None,
                name="log_to_mlflow_node",
            ),
        ]
    )
