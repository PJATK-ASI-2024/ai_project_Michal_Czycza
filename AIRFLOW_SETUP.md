# Instrukcja Uruchomienia Airflow dla Projektu

## Szybki Start

### 1. Uruchom Docker Compose

```powershell
cd C:\Users\micha\Desktop\ai_project_Michal_Czycza
docker-compose up -d
```

### 2. Sprawdź Status

```powershell
docker-compose ps
```

Wszystkie kontenery powinny mieć status "Up" lub "Exit 0" (airflow-init).

### 3. Otwórz Airflow UI

Otwórz przeglądarkę i przejdź do: **http://localhost:8080**

**Dane logowania:**
- Username: `admin`
- Password: `admin`

### 4. Uruchom DAG

1. W Airflow UI znajdź DAG o nazwie **kedro_project_pipeline**
2. Włącz DAG (przełącznik po lewej stronie)
3. Kliknij **Trigger DAG** (ikona ▶️ po prawej)
4. Obserwuj postęp w Graph View lub Tree View

## Struktura Pipeline'u

```
EDA → Preprocessing → Modeling → Evaluation
```

- **EDA**: Analiza eksploracyjna (~5s)
- **Preprocessing**: Przygotowanie danych (~7s)
- **Modeling**: Trening 3 modeli (~25s)
- **Evaluation**: K-fold CV + metryki (~12s)

**Całkowity czas:** ~50 sekund

## Monitorowanie

### Logi w czasie rzeczywistym

```powershell
# Wszystkie logi
docker-compose logs -f

# Tylko webserver
docker-compose logs -f airflow-webserver

# Tylko scheduler
docker-compose logs -f airflow-scheduler
```

### Sprawdź status tasków

W Airflow UI:
- **Graph View**: Wizualizacja przepływu
- **Tree View**: Historia uruchomień
- **Gantt Chart**: Czas wykonania
- **Task Instance Details**: Szczegółowe logi

## Zatrzymanie i Czyszczenie

### Zatrzymaj kontenery

```powershell
docker-compose down
```

### Usuń wszystkie dane (świeży start)

```powershell
docker-compose down -v
```

### Restart konkretnego serwisu

```powershell
docker-compose restart airflow-webserver
docker-compose restart airflow-scheduler
```

## Rozwiązywanie Problemów

### Problem: Kontenery nie startują

```powershell
# Sprawdź logi
docker-compose logs airflow-webserver
docker-compose logs postgres

# Restart z czystą bazą
docker-compose down -v
docker-compose up -d
```

### Problem: DAG nie pojawia się w UI

```powershell
# Sprawdź logi schedulera
docker-compose logs airflow-scheduler

# Zrestartuj scheduler
docker-compose restart airflow-scheduler
```

### Problem: Task kończy się błędem

1. Kliknij na czerwony kwadrat taska w Graph View
2. Przejdź do **Log**
3. Sprawdź szczegóły błędu
4. Możesz spróbować ponownie: **Clear** → **Success/Failed** → **Trigger**

## Konfiguracja Harmonogramu

Aby włączyć automatyczne uruchamianie, edytuj `dags/kedro_dag.py`:

```python
# Przykłady:
schedule_interval="0 8 * * *"     # Codziennie o 8:00
schedule_interval="0 9 * * 1"     # W poniedziałki o 9:00
schedule_interval="@daily"        # Codziennie o północy
schedule_interval="@hourly"       # Co godzinę
```

## Dostęp do Danych

Wszystkie dane są dostępne w kontenerze pod `/opt/project/data/`:

```powershell
# Wejdź do kontenera
docker exec -it airflow-webserver bash

# Sprawdź dane
ls /opt/project/data/reporting/
```

## Porty

- **8080**: Airflow Web UI
- **5433**: PostgreSQL (mapowany z 5432)
- **6379**: Redis

## Zasoby

- **CPU**: 2 cores minimum
- **RAM**: 4GB minimum
- **Disk**: 10GB wolnej przestrzeni

---

**Pytania?** Sprawdź `docs/airflow_report.md` dla pełnej dokumentacji.
