1. Wybór tematu projektu

Problem do rozwiązania: rekomendacja filmów na podstawie tytułu filmu obejrzanego przez użytkownika (Content-Based Recommender System).

Wartość użytkowa: ułatwia użytkownikom odkrywanie filmów podobnych do tych, które już lubią; może być bazą dla systemów rekomendacji w serwisach streamingowych.

Dane: TMDB 5000 Movie Dataset (Kaggle): tmdb_5000_movies.csv i tmdb_5000_credits.csv.



Projekt architektury systemu

| Moduł                      | Opis                                         | Technologia  |
| -------------------------- | -------------------------------------------- | ------------ |
| ETL / przetwarzanie danych | Czyszczenie i przygotowanie danych filmowych | Kedro        | 
| Trening modelu             | Obliczanie podobieństwa między filmami       | scikit-learn |
| API backend                | Udostępnienie rekomendacji                   | FastAPI      |
| UI frontend                | Interaktywny interfejs użytkownika           | Streamlit    |
| Automatyzacja              | Uruchamianie pipeline’u ETL i retrainingu    | Airflow      |
| Wdrożenie                  | Konteneryzacja i deployment                  | Docker       |


Diagram architektury
![Diagram architektury](docs/architecture_diagram.png)



Członkowie zespołu
| Imię i nazwisko | Rola w projekcie  | GitHub login |
|  Michał Czycza  |     Właściciel    |   Mickelele  |
