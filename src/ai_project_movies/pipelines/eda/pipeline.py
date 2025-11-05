from kedro.pipeline import Pipeline, node
from .nodes import (
    merge_datasets,
    basic_stats,
    missing_data,
    plot_basic_distributions,
    correlation_heatmap,
    save_summary,
)

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=merge_datasets,
            inputs=["raw_movies", "raw_credits"],
            outputs="merged_data",
            name="merge_datasets"
        ),
        node(
            func=basic_stats,
            inputs="merged_data",
            outputs="stats",
            name="basic_stats"
        ),
        node(
            func=missing_data,
            inputs="merged_data",
            outputs="missing",
            name="missing_data"
        ),
        node(
            func=plot_basic_distributions,
            inputs="merged_data",
            outputs=None,
            name="plot_basic_distributions"
        ),
        node(
            func=correlation_heatmap,
            inputs="merged_data",
            outputs="corr",
            name="correlation_heatmap"
        ),
        node(
            func=save_summary,
            inputs=["stats", "missing"],
            outputs=None,
            name="save_summary"
        ),
    ])
