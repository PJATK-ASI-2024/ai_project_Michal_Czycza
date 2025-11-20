from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    prepare_features,
    train_baseline_model,
    evaluate_baseline_model,
    train_automl_model,
    train_custom_model,
    evaluate_custom_model,
    compare_models,
    select_best_model,
    evaluate_final_model,
    plot_model_comparison 
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
         
            node(
                func=prepare_features,
                inputs=["train_data", "val_data", "test_data"],
                outputs=["all_data", "movie_titles", "features"],
                name="prepare_features_node",
            ),

     
            node(
                func=train_baseline_model,
                inputs=["features"],
                outputs="baseline_model",
                name="train_baseline_node",
            ),
            node(
                func=evaluate_baseline_model,
                inputs=["baseline_model", "movie_titles"],
                outputs="baseline_metrics",
                name="evaluate_baseline_node",
            ),
            
           
            node(
                func=train_automl_model,
                inputs=["features"],
                outputs=["automl_model", "automl_metrics", "automl_results"],
                name="train_automl_node",
            ),
            
         
            node(
                func=train_custom_model,
                inputs=["features"],
                outputs="custom_model",
                name="train_custom_node",
            ),
            node(
                func=evaluate_custom_model,
                inputs=["custom_model", "movie_titles"],
                outputs="custom_metrics",
                name="evaluate_custom_node",
            ),
            
    
            node(
                func=compare_models,
                inputs=["baseline_metrics", "automl_metrics", "custom_metrics"],
                outputs="model_comparison",
                name="compare_models_node",
            ),
            node(
                func=select_best_model,
                inputs=[
                    "baseline_model",
                    "automl_model", 
                    "custom_model",
                    "baseline_metrics",
                    "automl_metrics",
                    "custom_metrics"
                ],
                outputs="best_model",
                name="select_best_model_node",
            ),
            
       
            node(
                func=evaluate_final_model,
                inputs=["best_model", "movie_titles", "all_data"],
                outputs="final_test_metrics",
                name="evaluate_final_node",
            ),
            

            node(
                func=plot_model_comparison,
                inputs=["model_comparison", "params:model_comparison_output_dir"],
                outputs=None,
                name="plot_model_comparison_node",
            ),
        ]
    )