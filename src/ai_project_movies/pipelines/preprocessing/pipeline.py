from kedro.pipeline import Pipeline, node
from .nodes import merge_datasets, clean_data, scale_data, split_data

def create_pipeline(**kwargs):
    return Pipeline([
        node(func=merge_datasets,
             inputs=["raw_movies", "raw_credits"],
             outputs="merged_data",
             name="merge_datasets_node"),

        node(func=clean_data,
             inputs="merged_data",
             outputs="clean_data",
             name="clean_data_node"),

        node(func=scale_data,
             inputs="clean_data",
             outputs="scaled_data",
             name="scale_data_node"),

        node(func=split_data,
             inputs="scaled_data",
             outputs=["train_data", "val_data", "test_data"],
             name="split_data_node"),
    ])
