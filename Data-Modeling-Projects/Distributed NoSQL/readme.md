# Distributed NoSQL Database Project

## Overview
Welcome to the Distributed NoSQL Database Project! This project combines the power of a relational database with Apache Cassandra, a distributed NoSQL database. This README aims to provide an overview of the project's structure, purpose, and key components.

## Project Structure
- **ETL Pipeline**: Pre-processes files and creates a CSV file (`event_datafile_new.csv`) for Apache Cassandra tables.
- **Apache Cassandra Coding**: Creates a cluster, keyspace, tables, inserts data, and runs queries in Apache Cassandra.
- **Data Files**:
  - `event_data/`: Contains 30 CSV files with event data for preprocessing.
  - `event_datafile_new.csv`: CSV file generated from preprocessing for Apache Cassandra tables.
- **Notebook**: `Project_Distributed_NoSQL.ipynb`: Jupyter Notebook containing code, documentation, and explanations for the project.

## Key Concepts
- **Data Flexibility**: NoSQL modeling allows for dynamic and evolving data structures.
- **Scalability**: Apache Cassandra's distributed architecture enables horizontal scaling for large-scale data storage and processing.
- **Query Optimization**: Data modeling in NoSQL focuses on optimizing queries for fast and efficient data retrieval.

## Getting Started
1. Run the ETL Pipeline to preprocess files and generate `event_datafile_new.csv`.
2. Execute Apache Cassandra Coding scripts in the notebook to create tables, insert data, and run queries.
3. Explore NoSQL modeling concepts and optimize queries for performance.

## Credits
This project is part of learning NoSQL modeling and integrating Apache Cassandra into a database system. Feel free to modify and expand upon the code and concepts presented here.

Happy coding!
