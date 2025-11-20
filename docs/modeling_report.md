# Modeling Report — Movie Recommendation System  
---

## 1. Cel projektu

Celem etapu modelowania było zbudowanie, porównanie oraz automatyzacja procesu treningu trzech modeli rekomendacji filmów:

1. **Model bazowy (Baseline)**
2. **Model AutoML**
3. **Własny model (Custom)**

Dodatkowo przygotowano:
- pełny pipeline w Kedro,
- zapis modeli i metryk,
- wybór najlepszego modelu,
- finalny test rekomendacji,
- wizualizacje wyników.

---

## 2. Dane użyte w modelowaniu

Wykorzystano przygotowane wcześniej dane:
- `train.parquet`
- `val.parquet` 
- `test.parquet`

Łącznie połączone w `all_data` (4800 filmów).

Do cechowania wykorzystano kolumny tekstowe:
- `title`
- `overview` 
- `genres`
- `keywords`

Tworzona była jedna kolumna: **combined_features**.

---

## 3. Zastosowane modele

### **3.1 Baseline**
Model TF-IDF:
- max_features = 1500
- ngram_range = (1, 1)
- stop_words = english  
- cosine similarity

### **3.2 AutoML** 
Grid search po:
- max_features: [500, 2000, 5000]
- ngram_range: [(1,1), (1,2)]
- min_df: [1,3,5]

Model wybierany na podstawie własnej metryki:  
**score = avg_similarity·0.7 + matrix_density·0.3**

**Najlepsze parametry AutoML:** max_f=500, ngram=(1, 2), min_df=1

### **3.3 Custom Model**
Zaawansowany TF-IDF:
- max_features = 8000  
- ngram_range = (1, 2)  
- min_df = 3  
- max_df = 0.7  
- use_idf = True  
- smooth_idf = True  
- sublinear_tf = True  

---

## 4. Porównanie metryk modeli

### Wykresy porównawcze

![Porównanie metryk](data/08_reporting/plots/metrics_comparison.png)
*Rysunek 1: Kompleksowe porównanie wszystkich metryk*

![Average Similarity](data/08_reporting/plots/avg_similarity.png)
*Rysunek 2: Porównanie średniego podobieństwa między modelami*

![Matrix Density](data/08_reporting/plots/matrix_density.png)  
*Rysunek 3: Gęstość macierzy podobieństwa*

![Success Rate](data/08_reporting/plots/success_rate.png)
*Rysunek 4: Wskaźnik trafności rekomendacji*

### Tabela metryk

| Model | Avg Similarity | Matrix Density | Success Rate | Model Type |
|-------|----------------|----------------|--------------|------------|
| **Baseline** | 0.025 | 0.040 | **1.00** | TF-IDF |
| **AutoML** | **0.042** | **0.126** | 0.85 | Optimized TF-IDF |
| **Custom** | 0.014 | 0.008 | **1.00** | Advanced TF-IDF |

---

## 5. Wybór najlepszego modelu

Najlepszy model wybrano na podstawie metryki:  

### 🎯 **Success Rate (trafność rekomendacji)**

**Najlepszy model:**  
> **Baseline**

**Uzasadnienie:**  
Model Baseline osiągnął perfekcyjny wskaźnik trafności (100%) przy zachowaniu dobrych wartości podobieństwa i gęstości.

**Parametry zwycięskiego modelu:**
- max_features = 1500
- ngram_range = (1, 1) 
- stop_words = english

---

## 6. Analiza wyników AutoML

### Top 5 konfiguracji AutoML:

| Parameters | Score | Avg Similarity | Density |
|------------|-------|----------------|---------|
| max_f=500, ngram=(1, 2), min_df=1 | 0.0674 | 0.0422 | 0.1262 |
| max_f=500, ngram=(1, 2), min_df=3 | 0.0673 | 0.0421 | 0.1261 |
| max_f=500, ngram=(1, 2), min_df=5 | 0.0673 | 0.0421 | 0.1260 |
| max_f=500, ngram=(1, 1), min_df=1 | 0.0639 | 0.0410 | 0.1174 |
| max_f=500, ngram=(1, 1), min_df=3 | 0.0639 | 0.0409 | 0.1174 |

**Wnioski z AutoML:**
- Mniejsze wartości max_features (500) dają lepsze wyniki
- Bigramy ((1,2)) poprawiają jakość rekomendacji
- Minimal document frequency nie ma dużego wpływu

---

## 7. Finalna ewaluacja - przykładowe rekomendacje

### Przykład 1: "Desert Dancer"
**Rekomendacje:**
1. Flashdance (0.595)
2. Showgirls (0.552) 
3. Take the Lead (0.537)
4. Center Stage (0.436)
5. ABCD (Any Body Can Dance) (0.408)

### Przykład 2: "The Age of Innocence"  
**Rekomendacje:**
1. Cheri (0.391)
2. Metropolitan (0.384)
3. Mary Reilly (0.364)
4. The Elephant Man (0.356)
5. The Love Letter (0.347)

### Przykład 3: "Body Double"
**Rekomendacje:**
1. Tootsie (0.270)
2. An American in Hollywood (0.261)
3. Stuck on You (0.238)
4. Wonderland (0.233)
5. Spring Breakers (0.226)

---

## 8. Wnioski

### 📊 **Analiza porównawcza:**

1. **Baseline vs AutoML**:
   - AutoML ma wyższe podobieństwo (0.042 vs 0.025) i gęstość (0.126 vs 0.040)
   - Baseline ma lepszą trafność (100% vs 85%)
   - **Baseline wygrywa dzięki perfekcyjnej trafności**

2. **Custom Model**:
   - Najniższe wartości podobieństwa i gęstości
   - Perfekcyjna trafność (100%)
   - Zbyt agresywne parametry TF-IDF ograniczają jakość

3. **Trade-off między metrykami**:
   - Wyższe podobieństwo ↔ niższa trafność
   - Gęstość macierzy nie koreluje bezpośrednio z trafnością
   - **Trafność jest najważniejszą metryką biznesową**

---
