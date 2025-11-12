# Raport Preprocessing - Projekt AI Movies

## Opis datasetu
- **Źródło**: TMDB Movie Metadata (Kaggle)
- **Pliki źródłowe**: `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`
- **Rozmiar oryginalny**: 4803 filmy
- **Rozmiar po czyszczeniu**: 4800 filmów
- **Podział**: 3360 train (70%), 720 validation (15%), 720 test (15%)

## Cel preprocessingu
Przygotowanie danych do systemu rekomendacji filmów poprzez:
- Czyszczenie i standaryzację danych
- Ekstrakcję cech tekstowych
- Przygotowanie zbiorów treningowych, walidacyjnych i testowych

## Transformacje danych

### 1. Łączenie danych
- **Pliki wejściowe**: `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`
- **Klucz łączenia**: `id` (movies) ↔ `movie_id` (credits)
- **Typ łączenia**: LEFT JOIN
- **Rozwiązanie konfliktów**: 
  - Kolumna `title_x` (z movies) przemianowana na `title`
  - Kolumna `title_y` (z credits) usunięta

### 2. Przetwarzanie kolumn JSON
Kolumnę `combined_features` utworzono poprzez połączenie:
- **`title`** - tytuł filmu
- **`overview`** - opis filmu  
- **`genres`** - lista gatunków (wyodrębniona z JSON)
- **`keywords`** - słowa kluczowe (wyodrębnione z JSON)

Przetworzone kolumny JSON:
- **`genres`**: Wyodrębnienie nazw gatunków z formatu `[{"id": 1, "name": "Action"}]`
- **`keywords`**: Wyodrębnienie słów kluczowych
- **`cast`**: Pierwszych 5 aktorów
- **`crew`**: Tylko reżyserzy

### 3. Czyszczenie danych
- **Usunięto duplikaty**: 3 rekordy (4803 → 4800) po kolumnie `id`
- **Usunięto brakujące wartości**: Wiersze bez `title` lub `overview`
- **Uzupełnienie wartości numerycznych**:
  - `popularity`, `vote_average`, `vote_count` - mediana
  - Konwersja na typ numeric z obsługą błędów (`pd.to_numeric` z `errors="coerce"`)
- **Uzupełnienie wartości tekstowych**: Puste stringi dla pozostałych kolumn

### 4. Standaryzacja
- **Algorytm**: `StandardScaler` z `sklearn.preprocessing`
- **Kolumny**: `popularity`, `vote_average`, `vote_count`
- **Efekt**: Średnia = 0, Odchylenie standardowe = 1
- **Cel**: Przygotowanie dla algorytmów wrażliwych na skalę (SVM, regresja)

### 5. Podział danych
- **Proporcje**: 70% train, 15% validation, 15% test
- **Random state**: 42 (dla reprodukowalności)
- **Biblioteka**: `train_test_split` z `sklearn.model_selection`

## Technologie i narzędzia

### Biblioteki Python
- **pandas** - manipulacja danymi
- **numpy** - operacje numeryczne  
- **scikit-learn** - preprocessing i podział danych
- **ast** - parsowanie JSON

### Framework
- **Kedro** - zarządzanie pipeline'ami danych
- **pytest** - testy jednostkowe

### Format danych
- **Parquet** - format wyjściowy (zamiast CSV ze względu na problemy z kodowaniem)

## Metryki jakości

### Przed preprocessingem
- **Rozmiar**: 4803 rekordy
- **Brakujące wartości**: ~0.06% w kluczowych kolumnach
- **Duplikaty**: 3 rekordy

### Po preprocessingie  
- **Rozmiar**: 4800 rekordów
- **Brakujące wartości**: 0%
- **Zbalansowanie**: Zachowany oryginalny rozkład
- **Standaryzacja**: Wszystkie cechy numeryczne przeskalowane

## Pipeline Kedro

### Struktura pipeline'u
```python
Pipeline([
    node(merge_datasets, "raw_movies,raw_credits", "merged_data"),
    node(clean_data, "merged_data", "clean_data"), 
    node(scale_data, "clean_data", "scaled_data"),
    node(split_data, "scaled_data", ["train_data", "val_data", "test_data"])
])

