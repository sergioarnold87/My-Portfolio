# Project ClimateHappinessAnalytics

### Project Scope

This project combines data from Twitter, AWS Comprehend, and static data sources, including the world happiness report and earth surface temperature data. The goal is to work with batch and/or streaming data from Twitter, determine the sentiment of tweets, and combine that information with data related to the happiness score of a country and climate (temperature) changes over several decades. The resulting data model allows for analysis of relationships between tweets, sentiment, user locations, happiness scores, and temperature variations.

### Implementation Details

To gather data from Twitter, the project accesses its API using tweepy. Historical tweets are collected using `search_tweets.py`, and sentiment analysis is performed using AWS Comprehend. The scripts can be run locally or deployed to a cloud server/container (e.g., AWS EC2 or ECS). AWS Kinesis is used to ingest tweet data into S3 before staging it into Redshift. Airflow is employed to create tables in Redshift, stage data, and derive fact and dimension tables (`airflow/capstone_dag.py`).

The resulting star-schema based data model includes tables such as `staging_tweets`, `staging_happiness`, `staging_temperature`, `users`, `sources`, `happiness`, `temperature`, and `tweets`.

### Data Quality

A data quality assessment of static datasets and a sample of tweets was performed. The static datasets have no duplicates or missing values, but the temperature data contains about 4% missing values. Missing values in temperature data were dropped before uploading to S3. Tweet data is generally fine, but user locations lack standardization, making it challenging to join with happiness and/or temperature data.

### Handling Alternative Scenarios

Strategies for handling scenarios like a 100x increase in data, running the data pipeline daily, and simultaneous access by 100+ users are discussed. Solutions involve scaling resources, scheduling data loads, and precomputing complex queries.

### Prerequisites

Prerequisites include accounts for Twitter developer, Kaggle, and AWS, along with access to Kinesis Firehose and AWS Comprehend. A running AWS Redshift cluster, Airflow, and a Unix-like environment are required.

### Technology Stack

- **Programming Languages:**
  - Python
  - SQL

- **Data Processing and Storage:**
  - AWS Kinesis
  - AWS S3
  - AWS Redshift

- **Data Analysis and Visualization:**
  - pandas
  - Matplotlib
  - seaborn

- **Workflow Orchestration:**
  - Apache Airflow

- **API Integration:**
  - tweepy (Twitter API)
  - boto3 (AWS SDK for Python)

### Usage

Instructions for setting up the project, dependencies, and usage are provided in the README. They cover setting up connections, creating Python environments, obtaining datasets, running scripts, and triggering Airflow DAGs.

### Limitations

Limitations include non-standardized Twitter user locations and basic error handling in scripts. Manual setup of AWS tools is required.


