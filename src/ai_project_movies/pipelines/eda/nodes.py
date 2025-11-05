# src/ai_project_movies/pipelines/eda/nodes.py

import logging
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

log = logging.getLogger(__name__)

def merge_datasets(raw_movies: pd.DataFrame, raw_credits: pd.DataFrame) -> pd.DataFrame:
    """Łączy oba zbiory po id."""
    log.info(f"Movies shape: {raw_movies.shape}, Credits shape: {raw_credits.shape}")
    raw_credits = raw_credits.rename(columns={"movie_id": "id"})
    df = pd.merge(raw_movies, raw_credits, on="id", how="inner")
    log.info(f"Merged data shape: {df.shape}")
    return df

def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.describe(include="all").T
    log.info("Computed basic statistics")
    return stats

def missing_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum().sort_values(ascending=False)
    log.info("Calculated missing values")
    return missing.to_frame("missing_count")

def plot_basic_distributions(df: pd.DataFrame, output_dir="docs/figures") -> None:
    os.makedirs(output_dir, exist_ok=True)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    for col in numeric_cols[:6]:
        plt.figure(figsize=(10, 4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Histogram: {col}")
        plt.savefig(f"{output_dir}/{col}_hist.png")
        plt.close()

    cat_cols = df.select_dtypes(include="object").columns.tolist()
    for col in cat_cols[:4]:
        plt.figure(figsize=(8, 4))
        df[col].value_counts().head(10).plot(kind="bar")
        plt.title(f"Top values for {col}")
        plt.savefig(f"{output_dir}/{col}_bar.png")
        plt.close()
    log.info("Saved plots")

def correlation_heatmap(df: pd.DataFrame, output_path="docs/figures/correlation.png") -> pd.DataFrame:
    corr = df.select_dtypes(include=np.number).corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False)
    plt.title("Correlation heatmap")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    log.info("Saved correlation heatmap")
    return corr

def save_summary(stats: pd.DataFrame, missing: pd.DataFrame, output_dir="docs") -> None:
    os.makedirs(output_dir, exist_ok=True)
    stats.to_csv(f"{output_dir}/stats.csv")
    missing.to_csv(f"{output_dir}/missing.csv")
    with open(f"{output_dir}/eda_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Stats shape: {stats.shape}\n")
        f.write(f"Missing shape: {missing.shape}\n")
    log.info("Saved EDA summary")
