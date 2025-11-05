from ai_project_movies.pipelines import eda as eda_pipeline

def register_pipelines():
    return {
        "eda": eda_pipeline.create_pipeline()
    }
