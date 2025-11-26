# Copilot Instructions for AI Project Movies

## Project Overview
A **Content-Based Movie Recommender System** built with Kedro that recommends similar movies based on user input. Uses TMDB 5000 dataset to compute cosine similarity between movies based on combined text features (title, overview, genres, keywords, cast, directors).

## Architecture & Data Flow

### Four Pipelines (Zajęcia 1-5)
1. **Preprocessing** (`src/ai_project_movies/pipelines/preprocessing/`)
   - Merges raw TMDB CSV files → extracts list-type fields from JSON strings → creates combined text features → scales data → splits into train/val/test
   - Key nodes: `merge_datasets` → `clean_data` → `scale_data` → `split_data`
   - Output: Parquet files in `data/model_input/`

2. **Modeling** (`src/ai_project_movies/pipelines/modeling/`) - **CURRENTLY ACTIVE**
   - Trains 3 models: baseline (TF-IDF + cosine similarity), AutoML (PyCaret), custom (scikit-learn)
   - Evaluates similarity matrices and rankings
   - Selects best model and generates comparison plots
   - Outputs: Models as `.pkl`, metrics as `.json`, plots to `data/08_reporting/plots/`

3. **Evaluation** (`src/ai_project_movies/pipelines/evaluation/`) - **NEW (Zajęcia 5)**
   - Cross-validation (K-Fold) na train/val/test
   - Test set evaluation z metrykami dla rekomendacji (Recall@K, NDCG@K, MAP@K)
   - Feature importance analysis (TF-IDF weights)
   - Model versioning (CSV + MLflow)
   - Outputs: CV/test metrics to `data/reporting/`, model versions to CSV, logging to MLflow

4. **EDA** (`src/ai_project_movies/pipelines/eda/`)
   - Generates exploratory statistics, histograms, correlation heatmap
   - **Currently disabled** in `src/ai_project_movies/pipeline_registry.py` due to import issues

### Key Data Structures
- **Catalog** (`conf/base/catalog.yml`): Defines all data I/O (inputs/outputs, paths, formats)
- **Parameters** (`conf/base/parameters.yml`): Configuration like output directory
- **Input Data**: Two TMDB CSVs → merged on `id`/`movie_id`
- **Feature Engineering**: Concatenates title + overview + genres + keywords + cast + directors into single text field

## Working with Kedro

### Running Pipelines
```powershell
# Default (modeling pipeline - only active one)
kedro run

# Specific pipeline (if re-enabled)
kedro run --pipeline preprocessing
kedro run --pipeline eda

# View pipeline structure
kedro viz --help
```

### Development Workflow
- **Node Definition**: Functions in `nodes.py` that take typed inputs, return typed outputs
- **Pipeline Assembly**: In `pipeline.py`, connect nodes using `Pipeline([node(...), ...])` and `pipeline()` wrapper
- **Type Hints Required**: All node functions must have input/output type hints for Kedro's I/O resolution
- **Logging**: Use `logger = logging.getLogger(__name__)` for pipeline visibility

### Project Structure
```
src/ai_project_movies/
├── pipeline_registry.py       # Register active pipelines here
├── pipelines/
│   ├── preprocessing/pipeline.py + nodes.py
│   ├── modeling/pipeline.py + nodes.py
│   └── eda/pipeline.py + nodes.py
```

## Critical Implementation Patterns

### Text Processing & Feature Engineering
- **JSON string parsing**: Use `ast.literal_eval()` to convert JSON strings to lists
  ```python
  genres_list = [i['name'] for i in ast.literal_eval(genres_string)]
  ```
- **Error handling for malformed data**: Wrap in try/except, default to `[]`
- **Combined features**: Concatenate all text columns with spaces for TF-IDF vectorization

### Model Evaluation for Similarity-Based Systems
- Uses **cosine similarity matrix** not traditional metrics (no accuracy/F1 — this is unsupervised)
- Metrics tracked: matrix density, average similarity, max/min similarity
- **Ranking evaluation**: Tests if top-N recommendations are semantically coherent (manual validation)

### Data Handoff Between Pipelines
- Preprocessing outputs train/val/test as separate Parquet files → modeling reads all 3, concatenates, applies feature prep
- Modeling then splits into training and evaluation sets (not using preprocessing splits directly for model comparison)

## Testing & Validation

### Unit Tests Location
- `src/tests/pipelines/preprocessing/test_nodes.py` — Tests merge/clean/scale/split operations
- Pattern: Create mock DataFrames, call node function, assert output structure & values
- Key test: Verify JSON parsing works correctly, column conflicts resolved, combined features created

### Running Tests
```powershell
pytest src/tests/pipelines/preprocessing/test_nodes.py -v
```

## Zajęcia 5: Evaluation Pipeline & Model Versioning

### Running Evaluation Pipeline

```powershell
# Run only evaluation pipeline
kedro run --pipeline evaluation

# Run full pipeline (modeling + evaluation)
kedro run
```

### MLflow Tracking

```powershell
# Start MLflow UI
mlflow ui

# View dashboard at http://localhost:5000
```

### Model Versioning

Two approaches implemented:

1. **MLflow**: Automatic logging of metrics and parameters
2. **CSV Registry**: `data/reporting/model_versions.csv` - manual history tracking

Each model version records:
- Timestamp, version number
- CV metrics (Recall@K, NDCG@K, MAP@K)
- Test set metrics
- Top features and vocabulary size

### Output Files

```
data/reporting/
├── cv_results.json                     # Cross-validation metrics
├── test_evaluation_results.json        # Test set evaluation
├── feature_importance_results.json     # Top TF-IDF terms
├── model_version_record.json           # Current version metadata
└── model_versions.csv                  # Historical versions

docs/
├── model_evaluation_report.md          # Full analysis report (Zajęcia 5)
└── plots/
    ├── metrics_comparison.png
    ├── recall_at_k.png
    ├── feature_importance.png
    └── similarity_distribution.png
```

### Analysis Scripts

Generate visualizations automatically:

```powershell
python generate_error_analysis.py
```

Creates plots for:
- CV vs Test set comparison
- Recall@K curves
- Feature importance ranking
- Similarity score distribution
- Per-fold results

## Dependencies & Stack
- **Kedro 1.0+**: Orchestration framework
- **scikit-learn**: TF-IDF, cosine similarity, K-Fold cross-validation
- **PyCaret**: AutoML (used in modeling pipeline for automated feature selection & model comparison)
- **mlflow>=2.0.0**: Experiment tracking and model versioning (NEW - Zajęcia 5)
- **pandas/numpy**: Data manipulation
- **seaborn/matplotlib**: Visualization in EDA and modeling

## Metryki Dla Systemu Rekomendacji (Zajęcia 5)

Model oceniany jest za pomocą specjalnych metryk dla systemów rekomendacji (nie tradycyjnych ML metryk):

- **Recall@K**: Proporcja relewantnych elementów w top-K (próg relewancji: similarity > 0.3)
  - Recall@5 = % zapytań gdzie relewantny film jest w top-5
  - Recall@10 = % zapytań gdzie relewantny film jest w top-10

- **NDCG@K**: Normalized Discounted Cumulative Gain - jakość rangowania
  - Wyższe = relewantne filmy są wyżej na liście

- **MAP@K**: Mean Average Precision - średnia precyzja dla każdego K

Obserwowany wynik baseline'u:
- **Recall@5**: 0.65 (65% trafień w top-5)
- **Recall@10**: 0.79 (79% trafień w top-10)
- **NDCG@5**: 0.71 (dobre rangowanie)

## Known Issues & Workarounds

### Disabled Pipelines
- EDA and preprocessing pipelines currently **commented out** in `pipeline_registry.py`
- Reason: Import/dependency issues in those modules
- When re-enabling: Check that all node functions have correct type hints and that dependencies are installed

### Feature Column Handling
- TMDB data uses mixed formats: some columns are JSON strings, others are regular columns
- Always check column names after merge (naming conflicts like `title_x`/`title_y` possible) — see `merge_datasets()` handling

## Extension Points

When adding features:
1. Add new node to `nodes.py` with full type hints
2. Register node in pipeline's `pipeline.py` using `node()` function
3. Update `catalog.yml` if creating new artifacts
4. Add corresponding unit test in `src/tests/`

---

**Last Updated**: November 2025  
**Primary Stack**: Kedro, scikit-learn, PyCaret, pandas
