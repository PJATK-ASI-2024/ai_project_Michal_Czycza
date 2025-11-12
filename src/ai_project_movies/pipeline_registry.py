from ai_project_movies.pipelines import eda as eda_pipeline
from ai_project_movies.pipelines import preprocessing as preprocessing_pipeline

def register_pipelines():
    return {
        "eda": eda_pipeline.create_pipeline(),
        "preprocessing": preprocessing_pipeline.create_pipeline(),
    }
