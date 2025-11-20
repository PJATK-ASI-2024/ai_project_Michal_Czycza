def plot_model_comparison(metrics_path: str, output_dir: str):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import json
    import os

    print("=== LOADING METRICS FROM ===")
    print(metrics_path)
    print(os.path.abspath(metrics_path))

    print("=== OUTPUT DIR ===")
    print(output_dir)
    print(os.path.abspath(output_dir))

    sns.set(style="whitegrid")
    os.makedirs(output_dir, exist_ok=True)

    # === Wczytanie metryk ===
    with open(metrics_path, "r") as f:
        data = json.load(f)

    metrics = data["models"]  

    models = ["baseline", "automl", "custom"]

    avg_similarity = [metrics[m]["avg_similarity"] for m in models]
    matrix_density = [metrics[m]["matrix_density"] for m in models]
    success_rate = [metrics[m]["success_rate"] for m in models]

    # --- Average similarity ---
    plt.figure(figsize=(8,5))
    sns.barplot(x=models, y=avg_similarity)
    plt.title("Average Similarity")
    plt.ylabel("Similarity Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "avg_similarity.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Matrix density ---
    plt.figure(figsize=(8,5))
    sns.barplot(x=models, y=matrix_density)
    plt.title("Matrix Density")
    plt.ylabel("Density Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "matrix_density.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Success rate ---
    plt.figure(figsize=(8,5))
    sns.barplot(x=models, y=success_rate)
    plt.title("Success Rate")
    plt.ylabel("Success Rate")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "success_rate.png"), dpi=300, bbox_inches='tight')
    plt.close()

    print("=== LOADED MODEL KEYS ===")
    print(list(metrics.keys()))

    print("=== METRICS VALUES ===")
    print(f"Avg similarity: {avg_similarity}")
    print(f"Matrix density: {matrix_density}")
    print(f"Success rate: {success_rate}")

    print("=== SAVING PLOTS ===")
    print(f"Saved avg_similarity.png to {output_dir}")
    print(f"Saved matrix_density.png to {output_dir}")
    print(f"Saved success_rate.png to {output_dir}")

    print(f"Zapisano wykresy porównania metryk do {output_dir}")