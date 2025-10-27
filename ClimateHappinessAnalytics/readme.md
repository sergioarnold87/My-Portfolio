<div align="center">

# 🌍 Climate & Happiness Analytics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-017CEE?logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-Big%20Data-E25A1C?logo=apache-spark&logoColor=white)](https://spark.apache.org/)

**End-to-End Data Engineering Pipeline Analyzing Climate Impact on Global Happiness**

</div>

---

## 📖 Overview

This comprehensive data engineering project combines real-time Twitter sentiment analysis with historical climate and happiness data to explore correlations between environmental changes, social sentiment, and national well-being indicators. The system ingests, processes, and analyzes multi-source data using modern cloud-native data engineering practices.

The pipeline processes streaming social media data, performs sentiment analysis using AWS Comprehend, and integrates static datasets (World Happiness Report, Earth Surface Temperature Data) into a unified star-schema data warehouse built on AWS Redshift.

---

## 🏗️ Architecture / Pipeline

```
┌─────────────────┐
│  Twitter API    │
│   (Streaming)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  search_tweets  │────▶│  AWS Comprehend  │
│  stream_tweets  │     │ (Sentiment Anlys)│
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────┐
│         AWS Kinesis Firehose        │
│     (Real-time Data Ingestion)      │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│             AWS S3                  │
│     (Data Lake / Staging Area)      │
│  - tweets/ (streaming data)         │
│  - happiness/ (static data)         │
│  - temperature/ (historical data)   │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│        Apache Airflow DAG           │
│    (Orchestration & ETL Logic)      │
│  - Create staging tables            │
│  - Load data from S3                │
│  - Transform & model data           │
│  - Data quality checks              │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         AWS Redshift DW             │
│       (Star Schema Model)           │
│                                     │
│  Fact Tables:                       │
│    - tweets                         │
│                                     │
│  Dimension Tables:                  │
│    - users                          │
│    - sources                        │
│    - happiness                      │
│    - temperature                    │
└─────────────────────────────────────┘
```

### **Pipeline Flow:**

1. **Data Ingestion:** Twitter API streams real-time tweets via tweepy
2. **Sentiment Analysis:** AWS Comprehend analyzes tweet sentiment (positive/negative/neutral)
3. **Stream Processing:** AWS Kinesis Firehose ingests data into S3
4. **Data Lake:** S3 stores raw tweets + static datasets (happiness, temperature)
5. **ETL Orchestration:** Airflow DAG manages staging, transformation, and loading
6. **Data Warehouse:** Redshift hosts star-schema dimensional model for analytics
7. **Analytics:** Query layer enables cross-dataset analysis and visualization

---

## 🛠️ Tech Stack

### **Core Technologies**
- **Python 3.8+** - Primary programming language
- **Apache Airflow** - Workflow orchestration and scheduling
- **Apache Spark** - Big data processing (optional for large-scale batch jobs)

### **AWS Cloud Services**
- **AWS Kinesis Firehose** - Real-time data streaming
- **AWS S3** - Data lake and staging storage
- **AWS Redshift** - Cloud data warehouse
- **AWS Comprehend** - NLP sentiment analysis
- **AWS EC2/ECS** - Compute resources for scripts

### **Data & APIs**
- **Twitter API (tweepy)** - Social media data source
- **Kaggle Datasets** - World Happiness Report, Temperature Data
- **boto3** - AWS SDK for Python

### **Analysis & Visualization**
- **pandas** - Data manipulation
- **Matplotlib & Seaborn** - Data visualization
- **SQL** - Query language for Redshift

---

## 🚀 How to Run

### Prerequisites

```bash
# Required Accounts
- Twitter Developer Account (API credentials)
- AWS Account (Kinesis, S3, Redshift, Comprehend access)
- Kaggle Account (for datasets)

# System Requirements
- Python 3.8+
- Apache Airflow
- Unix-like environment (Linux Mint recommended)
```

### Installation

1. **Navigate to project directory:**
```bash
cd /home/sergio/my-project/My-Portfolio/ClimateHappinessAnalytics
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt

# Or use conda environment
conda env create -f capstone_env.yml
conda activate capstone_env
```

4. **Configure AWS credentials:**
```bash
# Set up AWS CLI
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

5. **Configure Twitter API credentials:**
```bash
# Create .env file or export variables
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
```

6. **Download datasets from Kaggle:**
```bash
# World Happiness Report
# Earth Surface Temperature Data
# Place in data/ directory
```

7. **Upload static data to S3:**
```bash
python upload_to_s3.py
```

8. **Run tweet collection scripts:**
```bash
# Historical tweets
python search_tweets.py

# Real-time streaming
python stream_tweets.py
```

9. **Start Airflow and trigger DAG:**
```bash
# Initialize Airflow DB
airflow db init

# Start scheduler
airflow scheduler

# Start webserver
airflow webserver --port 8080

# Trigger DAG
airflow dags trigger capstone_dag
```

---

## 💡 Key Learnings

### **Technical Insights:**
- **Real-time Data Engineering:** Implemented streaming ingestion pipeline with Kinesis Firehose
- **Cloud Data Warehousing:** Designed star-schema dimensional model in Redshift
- **Airflow Orchestration:** Built complex DAGs for ETL automation and monitoring
- **Sentiment Analysis:** Integrated AWS Comprehend for NLP at scale
- **Data Lake Architecture:** Structured multi-source data staging in S3

### **Best Practices:**
- Separation of concerns (ingestion → staging → transformation)
- Idempotent pipeline design for retry safety
- Data quality checks at each stage
- Scalable architecture for handling data volume increases
- Environment-based configuration management

### **Challenges Overcome:**
- **Non-standardized Locations:** Twitter user locations lack consistency; implemented fuzzy matching
- **Data Quality:** Handled ~4% missing values in temperature data through interpolation
- **API Rate Limits:** Implemented exponential backoff for Twitter API
- **Cost Optimization:** Balanced Redshift cluster sizing with query performance

---

## 📊 Data Model

### **Star Schema Design**

**Fact Table:**
- `tweets` - Central fact table with tweet metrics and foreign keys

**Dimension Tables:**
- `users` - Twitter user demographics
- `sources` - Tweet source/device information
- `happiness` - Country happiness scores by year
- `temperature` - Historical temperature data by location

**Staging Tables:**
- `staging_tweets` - Raw tweet data from S3
- `staging_happiness` - Raw happiness report data
- `staging_temperature` - Raw climate data

---

## 📁 Project Structure

```
ClimateHappinessAnalytics/
├── airflow/
│   └── capstone_dag.py       # Main Airflow DAG
├── sql/
│   ├── create_tables.sql     # DDL statements
│   └── analytics_queries.sql # Sample analytics queries
├── notebooks/
│   ├── EDA.ipynb            # Exploratory data analysis
│   └── visualization.ipynb   # Results visualization
├── data/                     # Local datasets (gitignored)
├── search_tweets.py          # Historical tweet collector
├── stream_tweets.py          # Real-time tweet streamer
├── upload_to_s3.py          # S3 upload utility
├── requirements.txt          # Python dependencies
├── capstone_env.yml         # Conda environment file
├── data dictionary.md        # Data schema documentation
└── README.md                # This file
```

---

## 🔍 Sample Analytics Queries

```sql
-- Average happiness score by temperature range
SELECT 
    CASE 
        WHEN t.temperature < 10 THEN 'Cold'
        WHEN t.temperature BETWEEN 10 AND 25 THEN 'Moderate'
        ELSE 'Hot'
    END as temp_range,
    AVG(h.happiness_score) as avg_happiness
FROM tweets tw
JOIN happiness h ON tw.country = h.country AND tw.year = h.year
JOIN temperature t ON tw.country = t.country AND tw.year = t.year
GROUP BY temp_range;

-- Sentiment distribution by country happiness rank
SELECT 
    h.country,
    h.happiness_rank,
    COUNT(CASE WHEN tw.sentiment = 'POSITIVE' THEN 1 END) as positive_tweets,
    COUNT(CASE WHEN tw.sentiment = 'NEGATIVE' THEN 1 END) as negative_tweets
FROM tweets tw
JOIN happiness h ON tw.country = h.country
GROUP BY h.country, h.happiness_rank
ORDER BY h.happiness_rank;
```

---

## 🔮 Future Enhancements

- [ ] Implement Apache Spark for large-scale batch processing
- [ ] Add real-time dashboard using Tableau/PowerBI
- [ ] Integrate additional data sources (economic indicators, pollution data)
- [ ] Implement machine learning models for happiness prediction
- [ ] Add data lineage tracking and observability
- [ ] Automate infrastructure provisioning with Terraform
- [ ] Deploy containerized architecture with Docker/Kubernetes

---

## 📝 License

This project is part of the [Sergio Arnold Portfolio](../) and follows the repository's license.

---

<div align="center">

**Built with 🌍 and 📊 by [Sergio Arnold](https://github.com/sergioarnold87)**

[⬅️ Back to Portfolio](../)

</div>


