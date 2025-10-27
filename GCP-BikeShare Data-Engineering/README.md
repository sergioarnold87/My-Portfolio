<div align="center">

# 🚴 GCP BikeShare Data Engineering Pipeline

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?logo=google-bigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Cloud Storage](https://img.shields.io/badge/Cloud%20Storage-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/storage)

**End-to-End Data Engineering Pipeline for BikeShare Analytics on Google Cloud Platform**

</div>

---

## 📖 Overview

This project demonstrates a complete data engineering solution built on **Google Cloud Platform (GCP)** for analyzing bike-sharing operational data. The pipeline ingests raw data from **Cloud Storage**, processes it through **BigQuery**, and creates a dimensional data warehouse following modern data engineering best practices.

The solution implements a **medallion architecture** with three layers:
- **Raw Layer** (`raw_bikesharing`): Landing zone for unprocessed data
- **Data Warehouse Layer** (`dwh_bikesharing`): Cleaned, transformed dimensional model
- **Data Mart Layer** (`dm_bikesharing`): Business-ready analytical views

**Use Cases:**
- Station utilization analysis
- Trip pattern identification
- Demand forecasting
- Operational optimization
- Regional performance comparison

---

## 🏗️ Architecture / Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Trips   │  │ Stations │  │ Regions  │                  │
│  │  (JSON)  │  │  (CSV)   │  │  (CSV)   │                  │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘                  │
└────────┼────────────┼─────────────┼────────────────────────┘
         │            │             │
         ▼            ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│               GOOGLE CLOUD STORAGE (GCS)                     │
│              gs://project-data-bucket/                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Load Jobs
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   BIGQUERY - RAW LAYER                       │
│              Dataset: raw_bikesharing                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  trips   │  │ stations │  │ regions  │                  │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘                  │
└────────┼────────────┼─────────────┼────────────────────────┘
         │            │             │
         │   ETL Transformations (Python + SQL)               │
         ▼            ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│              BIGQUERY - DATA WAREHOUSE LAYER                 │
│              Dataset: dwh_bikesharing                        │
│                                                              │
│  ┌─────────────────────────────────────────────┐            │
│  │         FACT TABLE                          │            │
│  │   fact_trips_daily                          │            │
│  │   - trip_date                               │            │
│  │   - start_station_id (FK)                   │            │
│  │   - total_trips                             │            │
│  │   - sum_duration_sec                        │            │
│  │   - avg_duration_sec                        │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
│  ┌────────────────────┐    ┌───────────────────┐           │
│  │  DIMENSION TABLE   │    │  DIMENSION TABLE  │           │
│  │  dim_stations      │    │   dim_regions     │           │
│  │  - station_id (PK) │    │  - region_id (PK) │           │
│  │  - station_name    │    │  - region_name    │           │
│  │  - region_name     │    │                   │           │
│  │  - capacity        │    │                   │           │
│  └────────────────────┘    └───────────────────┘           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Analytical Views
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              BIGQUERY - DATA MART LAYER                      │
│              Dataset: dm_bikesharing                         │
│  ┌──────────────────────────────────────────┐               │
│  │  Business Intelligence Views              │               │
│  │  - Daily metrics by station               │               │
│  │  - Regional performance                   │               │
│  │  - Usage trends                           │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### **Core Technologies**
- **Python 3.8+** - Primary programming language
- **Google Cloud SDK (gcloud)** - CLI for GCP resource management

### **Google Cloud Platform Services**
- **BigQuery** - Cloud data warehouse for analytics
- **Cloud Storage (GCS)** - Object storage for data lake
- **Cloud SQL** - Relational database (optional staging)
- **IAM** - Identity and access management

### **Python Libraries**
- **google-cloud-bigquery** - BigQuery Python client
- **google-cloud-storage** - Cloud Storage client
- **pandas** - Data manipulation (for local testing)

### **Data Architecture**
- **Medallion Architecture** - Bronze (Raw) → Silver (DWH) → Gold (DM)
- **Star Schema** - Dimensional modeling with fact and dimension tables
- **Incremental Loads** - Date-partitioned data processing

---

## 📁 Project Structure

```
GCP-BikeShare Data-Engineering/
├── code/
│   ├── bigquery_scenario_2_step_0_create_datasets.py          # Create BQ datasets
│   ├── bigquery_scenario_2_step_1a_load_trips_data.py         # Load trips from GCS
│   ├── bigquery_scenario_2_step_1a_load_trips_data_20180102.py # Load trips (day 2)
│   ├── bigquery_scenario_2_step_1b_load_regions_data.py       # Load regions
│   ├── bigquery_scenario_2_step_2b_load_stations_data.py      # Load stations
│   ├── bigquery_scenario_2_step_3_create_dim_table_stations.py # Create dim_stations
│   ├── bigquery_scenario_2_step_3_create_fact_table_daily_trips.py # Create fact table
│   ├── bigquery_self_excercise_create_dim_table_regions.py    # Create dim_regions
│   ├── bigquery_self_excercise_create_fact_table_daily_by_gender_region.py
│   ├── bigquery_scenario_1_step_4_create_view_datamart.sql    # Create datamart views
│   ├── bigquery_self_excercise_query_answer.sql               # Sample analytical queries
│   ├── cloudsql_create_stations_table.sql                     # Cloud SQL setup
│   ├── gcloud_create_cloudsql_instance                        # Cloud SQL provisioning
│   ├── gcloud_export_cloudsql_to_gcs.sh                       # Export to GCS
│   └── gcloud_upload_local_file_to_gcs.sh                     # Upload data to GCS
│
├── dataset/
│   ├── regions/
│   │   └── regions.csv                                        # Region reference data
│   ├── stations/
│   │   └── stations.csv                                       # Station reference data
│   └── trips/
│       ├── 20180101/trips_20180101.json                       # Trip data (day 1)
│       └── 20180102/trips_20180102.json                       # Trip data (day 2)
│
├── README.md                                                   # This file
├── requirements.txt                                            # Python dependencies
├── .gitignore                                                  # Git ignore rules
└── config.yaml.example                                         # Configuration template
```

---

## 🚀 How to Run

### Prerequisites

```bash
# Google Cloud Platform
- GCP Project with billing enabled
- BigQuery API enabled
- Cloud Storage API enabled
- IAM permissions: BigQuery Admin, Storage Admin

# Local Environment
- Python 3.8+
- Google Cloud SDK installed
- Service account key (JSON)
```

### 1. Set Up GCP Environment

```bash
# Install Google Cloud SDK (if not already installed)
# https://cloud.google.com/sdk/docs/install

# Authenticate with GCP
gcloud auth login

# Set your project
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# Create service account
gcloud iam service-accounts create bikeshare-data-engineer \
    --display-name="BikeShare Data Engineer"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:bikeshare-data-engineer@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:bikeshare-data-engineer@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Download service account key
gcloud iam service-accounts keys create ~/bikeshare-key.json \
    --iam-account=bikeshare-data-engineer@${PROJECT_ID}.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=~/bikeshare-key.json
```

### 2. Create Cloud Storage Bucket

```bash
# Create GCS bucket
export BUCKET_NAME="${PROJECT_ID}-data-bucket"
gsutil mb -l US gs://${BUCKET_NAME}

# Upload dataset to GCS
bash code/gcloud_upload_local_file_to_gcs.sh
```

### 3. Install Python Dependencies

```bash
# Navigate to project directory
cd "/home/sergio/my-project/My-Portfolio/GCP-BikeShare Data-Engineering"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Update Configuration

```bash
# Update PROJECT_ID in all Python files
# Replace "packt-data-eng-on-gcp" with your project ID
sed -i 's/packt-data-eng-on-gcp/your-project-id/g' code/*.py
```

### 5. Run the Pipeline

```bash
# Step 1: Create BigQuery datasets
python code/bigquery_scenario_2_step_0_create_datasets.py

# Step 2: Load raw data from GCS to BigQuery
python code/bigquery_scenario_2_step_1b_load_regions_data.py
python code/bigquery_scenario_2_step_2b_load_stations_data.py
python code/bigquery_scenario_2_step_1a_load_trips_data.py

# Step 3: Create dimension tables
python code/bigquery_scenario_2_step_3_create_dim_table_stations.py
python code/bigquery_self_excercise_create_dim_table_regions.py

# Step 4: Create fact tables (provide date parameter)
python code/bigquery_scenario_2_step_3_create_fact_table_daily_trips.py 2018-01-01
python code/bigquery_scenario_2_step_3_create_fact_table_daily_trips.py 2018-01-02

# Step 5: Verify data in BigQuery
bq query --use_legacy_sql=false \
'SELECT * FROM `'$PROJECT_ID'.dwh_bikesharing.fact_trips_daily` LIMIT 10'
```

---

## 💡 Key Learnings

### **Technical Insights:**
- **BigQuery Partitioning:** Date-partitioned tables improve query performance and reduce costs
- **ELT vs ETL:** Leveraged BigQuery's processing power for transformations (ELT approach)
- **Medallion Architecture:** Separated raw, curated, and consumption layers for data governance
- **Incremental Loading:** Implemented date-based incremental loads to avoid reprocessing
- **Schema Evolution:** Designed flexible schemas to accommodate future data changes

### **GCP Best Practices:**
- **IAM Security:** Used service accounts with least-privilege access
- **Cost Optimization:** Leveraged partitioning and clustering to reduce query costs
- **Data Lake Design:** Organized GCS buckets with clear folder structures
- **Error Handling:** Implemented robust exception handling in Python scripts
- **Idempotency:** Designed scripts to be safely re-runnable

### **Challenges Overcome:**
- **Data Type Mismatches:** Handled CAST operations for region_id (INTEGER → STRING)
- **Date Filtering:** Correctly formatted date parameters for WHERE clauses
- **Bug Fixes:** Corrected variable naming errors (`project_id` → `PROJECT_ID`)
- **JOIN Logic:** Fixed incorrect table references in fact table creation

---

## 📊 Data Model

### **Dimensional Model (Star Schema)**

#### **Fact Table: fact_trips_daily**
- `trip_date` (DATE) - Date of trips
- `start_station_id` (STRING) - FK to dim_stations
- `total_trips` (INTEGER) - Count of trips
- `sum_duration_sec` (INTEGER) - Total trip duration
- `avg_duration_sec` (FLOAT) - Average trip duration

#### **Dimension Table: dim_stations**
- `station_id` (STRING) - PK
- `station_name` (STRING) - Station name
- `region_name` (STRING) - Associated region
- `capacity` (INTEGER) - Bike capacity

#### **Dimension Table: dim_regions**
- `region_id` (STRING) - PK
- `region_name` (STRING) - Region name

### **Sample Analytical Queries**

```sql
-- Top 10 busiest stations
SELECT 
    s.station_name,
    s.region_name,
    SUM(f.total_trips) as total_trips,
    AVG(f.avg_duration_sec)/60 as avg_duration_minutes
FROM `project-id.dwh_bikesharing.fact_trips_daily` f
JOIN `project-id.dwh_bikesharing.dim_stations` s
    ON f.start_station_id = s.station_id
GROUP BY s.station_name, s.region_name
ORDER BY total_trips DESC
LIMIT 10;

-- Daily trip trends
SELECT 
    trip_date,
    SUM(total_trips) as daily_trips,
    AVG(avg_duration_sec)/60 as avg_duration_minutes
FROM `project-id.dwh_bikesharing.fact_trips_daily`
GROUP BY trip_date
ORDER BY trip_date;

-- Regional performance comparison
SELECT 
    s.region_name,
    COUNT(DISTINCT s.station_id) as num_stations,
    SUM(f.total_trips) as total_trips,
    AVG(f.avg_duration_sec)/60 as avg_duration_minutes
FROM `project-id.dwh_bikesharing.fact_trips_daily` f
JOIN `project-id.dwh_bikesharing.dim_stations` s
    ON f.start_station_id = s.station_id
GROUP BY s.region_name
ORDER BY total_trips DESC;
```

---

## 🔧 Code Improvements Made

### **Bug Fixes:**
1. ✅ **Fixed variable name mismatch** in `load_trips_data.py` (line 5)
   - Changed `project_id` → `PROJECT_ID`
   
2. ✅ **Corrected JOIN clause** in `create_fact_table_daily_trips.py` (line 23)
   - Changed `{load_date}.raw_bikesharing.stations` → `{PROJECT_ID}.raw_bikesharing.stations`
   
3. ✅ **Fixed WHERE clause capitalization** (line 25)
   - Changed `WhERE` → `WHERE`
   
4. ✅ **Corrected date parameter usage** (line 25)
   - Changed `DATE('{}')` → `DATE('{load_date}')`

### **Code Enhancements:**
- Added comprehensive docstrings
- Improved error handling
- Standardized variable naming
- Added configuration examples

---

## 🔮 Future Enhancements

- [ ] **Airflow Integration:** Orchestrate pipeline with Apache Airflow
- [ ] **Data Quality Checks:** Implement Great Expectations for validation
- [ ] **Real-time Streaming:** Add Dataflow for real-time trip processing
- [ ] **dbt Integration:** Use dbt for SQL-based transformations
- [ ] **Monitoring & Alerting:** Set up Cloud Monitoring dashboards
- [ ] **Cost Optimization:** Implement BigQuery slot reservations
- [ ] **Data Catalog:** Use Data Catalog for metadata management
- [ ] **CI/CD Pipeline:** Automate deployment with Cloud Build
- [ ] **Machine Learning:** Add demand forecasting with Vertex AI
- [ ] **Looker Dashboard:** Create interactive BI dashboards

---

## 📝 License

This project is part of the [Sergio Arnold Portfolio](../) and follows the repository's license.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the main portfolio repository.

---

<div align="center">

**Built with ☁️ and 📊 by [Sergio Arnold](https://github.com/sergioarnold87)**

[⬅️ Back to Portfolio](../)

</div>
