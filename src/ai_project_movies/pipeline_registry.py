# Tymczasowo wyłącz EDA pipeline który ma problemy z importami
# from ai_project_movies.pipelines import eda as eda_pipeline
# from ai_project_movies.pipelines import preprocessing as preprocessing_pipeline
from ai_project_movies.pipelines import modeling as modeling_pipeline
from ai_project_movies.pipelines import evaluation as evaluation_pipeline

def register_pipelines():
    return {
        # "eda": eda_pipeline.create_pipeline(),
        # "preprocessing": preprocessing_pipeline.create_pipeline(),
        "modeling": modeling_pipeline.create_pipeline(),
        "evaluation": evaluation_pipeline.create_pipeline(),
        "__default__": modeling_pipeline.create_pipeline(),
    }