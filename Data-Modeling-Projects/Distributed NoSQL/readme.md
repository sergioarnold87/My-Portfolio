# Sparkify Data Modeling Project - Apache Cassandra

[![Cassandra](https://img.shields.io/badge/Apache%20Cassandra-3.11%2B-blue?logo=apache-cassandra&logoColor=white)](https://cassandra.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

## Project Overview

A production-ready **Query-First NoSQL Data Model** implementation using Apache Cassandra for Sparkify's music streaming analytics. This project demonstrates professional-level **distributed database modeling** with denormalized table structures optimized for specific query patterns, showcasing Cassandra's partition-based architecture and horizontal scalability.

### Key Features

✅ **Query-First Modeling** - Tables designed for specific access patterns  
✅ **Denormalization** - Data duplicated across tables for query optimization  
✅ **Partition Keys** - Optimized data distribution across cluster  
✅ **Clustering Keys** - Sorted data within partitions  
✅ **Horizontal Scalability** - Designed for distributed architecture  
✅ **Object-Oriented ETL** - Modular, reusable Python classes  
✅ **Comprehensive Logging** - Full pipeline observability  
✅ **Error Handling** - Robust exception management

## Apache Cassandra vs PostgreSQL

| Aspect | Cassandra (NoSQL) | PostgreSQL (Relational) |
|--------|-------------------|-------------------------|
| **Data Model** | Query-first, denormalized | Schema-first, normalized |
| **Scalability** | Horizontal (add nodes) | Vertical (bigger servers) |
| **Consistency** | Eventual consistency | ACID compliance |
| **Joins** | Not supported (denormalize) | Full JOIN support |
| **Schema** | Flexible, CQL-based | Rigid, SQL-based |
| **Use Case** | Write-heavy, distributed | Complex queries, transactions |

## Data Modeling Philosophy

### Query-First Approach

In Cassandra, **tables are designed around queries**, not entities:

```
Traditional (Relational)          Cassandra (NoSQL)
━━━━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━━
1. Design entities                1. Identify queries
2. Normalize data                 2. Design table per query
3. Create relationships           3. Denormalize data
4. Write queries with JOINs       4. No JOINs needed
```

### Three Query Patterns Implemented

#### Query 1: Session-based lookup
**Access Pattern:** "Get song details for a specific session and item"
```sql
SELECT artist, song_title, song_length 
FROM session_songs 
WHERE session_id = 338 AND item_in_session = 4;
```
**Table:** `session_songs`  
**Partition Key:** `session_id`  
**Clustering Key:** `item_in_session`

#### Query 2: User activity tracking
**Access Pattern:** "Get all songs for a user's session, sorted by play order"
```sql
SELECT artist, song, first_name, last_name
FROM user_songs
WHERE user_id = 10 AND session_id = 182;
```
**Table:** `user_songs`  
**Partition Key:** `(user_id, session_id)` - Composite partition key  
**Clustering Key:** `item_in_session DESC` - Reverse chronological order

#### Query 3: Song popularity analysis
**Access Pattern:** "Find all users who listened to a specific song"
```sql
SELECT first_name, last_name
FROM song_users
WHERE song = 'All Hands Against His Own';
```
**Table:** `song_users`  
**Partition Key:** `song`  
**Clustering Key:** `user_id`

## Table Schema Details

### Table 1: `session_songs`
```sql
CREATE TABLE session_songs (
    session_id INT,
    item_in_session INT,
    artist TEXT,
    song_title TEXT,
    song_length FLOAT,
    PRIMARY KEY (session_id, item_in_session)
);
```
**Why this design?**
- Partition by `session_id` - All items in a session stored together
- Cluster by `item_in_session` - Sorted playback order
- Fast lookup for session-based queries

### Table 2: `user_songs`
```sql
CREATE TABLE user_songs (
    user_id INT,
    session_id INT,
    item_in_session INT,
    artist TEXT,
    song TEXT,
    first_name TEXT,
    last_name TEXT,
    PRIMARY KEY ((user_id, session_id), item_in_session)
)
WITH CLUSTERING ORDER BY (item_in_session DESC);
```
**Why this design?**
- Composite partition key `(user_id, session_id)` - Unique user sessions
- Descending clustering order - Most recent plays first
- Enables user-session analytics

### Table 3: `song_users`
```sql
CREATE TABLE song_users (
    song TEXT,
    user_id INT,
    first_name TEXT,
    last_name TEXT,
    PRIMARY KEY (song, user_id)
);
```
**Why this design?**
- Partition by `song` - All listeners of a song together
- Cluster by `user_id` - Unique users per song
- Supports song popularity queries

## Key Cassandra Concepts Demonstrated

### 1. Denormalization
User data (`first_name`, `last_name`) is duplicated across tables. In Cassandra, **disk space is cheap, JOINs are expensive**.

### 2. Partition Keys
Determines data distribution across cluster nodes:
- Single partition: `session_id`
- Composite partition: `(user_id, session_id)`

### 3. Clustering Keys
Determines sort order within a partition:
- Ascending: Default behavior
- Descending: `WITH CLUSTERING ORDER BY (column DESC)`

### 4. Primary Key Structure
```
PRIMARY KEY = (Partition Key, Clustering Key)
              └─ Where data lives  └─ How data is sorted
```

## Installation & Setup

### Prerequisites

- **Apache Cassandra 3.11+** - [Installation Guide](https://cassandra.apache.org/doc/latest/getting_started/installing.html)
- **Python 3.8+**
- **pip** package manager

### Step 1: Install Apache Cassandra

**On Linux (Ubuntu/Debian):**
```bash
wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee /etc/apt/sources.list.d/cassandra.list
sudo apt update
sudo apt install cassandra
sudo service cassandra start
```

**Verify installation:**
```bash
nodetool status
```

### Step 2: Clone Repository

```bash
git clone <repository-url>
cd Data-Modeling-Projects/Distributed\ NoSQL
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run ETL Pipeline

**Option 1: Python Script**
```bash
python cassandra_etl.py
```

**Option 2: Jupyter Notebook**
```bash
jupyter notebook Project_Distributed_NoSQL.ipynb
```

## Usage Examples

### Python Script Execution

```python
from cassandra_etl import CassandraETL

# Initialize ETL pipeline
etl = CassandraETL(contact_points=['127.0.0.1'], keyspace='sparkify')

try:
    # Connect and setup
    etl.connect()
    etl.create_keyspace()
    etl.create_tables()
    
    # Process and load data
    csv_file = etl.preprocess_data()
    etl.load_data(csv_file)
    
    # Run sample queries
    etl.run_sample_queries()
    
finally:
    etl.close()
```

### CQL Shell Queries

```bash
# Connect to Cassandra
cqlsh

# Use keyspace
USE sparkify;

# Run queries
SELECT * FROM session_songs WHERE session_id = 338 AND item_in_session = 4;
SELECT * FROM user_songs WHERE user_id = 10 AND session_id = 182;
SELECT * FROM song_users WHERE song = 'All Hands Against His Own';
```

## File Structure

```
Distributed NoSQL/
├── cassandra_etl.py               # Production ETL pipeline
├── Project_Distributed_NoSQL.ipynb # Interactive notebook
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── readme.md                       # This file
├── event_data/                     # Raw CSV files (30 files)
├── event_datafile_new.csv          # Processed data
└── images/                         # Documentation images
```

## Technologies Used

- **Apache Cassandra** - Distributed NoSQL database
- **Python 3.8+** - ETL scripting
- **cassandra-driver** - Python Cassandra client
- **Pandas** - Data preprocessing
- **Jupyter** - Interactive development

## Best Practices Demonstrated

✅ Query-first data modeling  
✅ Denormalization for performance  
✅ Composite partition keys  
✅ Clustering order optimization  
✅ Object-oriented ETL design  
✅ Comprehensive error handling  
✅ Structured logging  
✅ Modular code architecture

## Data Modeling Anti-Patterns Avoided

❌ **No JOINs** - Data denormalized across tables  
❌ **No Secondary Indexes** - Partition keys designed for queries  
❌ **No Large Partitions** - Keys chosen to distribute data evenly  
❌ **No Unbounded Clustering** - Limited data per partition

## Performance Considerations

### Write Performance
- **Strength:** Cassandra excels at high-volume writes
- **Optimization:** Batch inserts for efficiency
- **Trade-off:** Data duplicated across tables (write amplification)

### Read Performance
- **Strength:** Single-partition reads are extremely fast
- **Optimization:** Partition keys match query patterns
- **Trade-off:** Multi-partition queries are slow (avoid ALLOW FILTERING)

### Scalability
- **Horizontal:** Add nodes without downtime
- **Replication:** Configurable replication factor
- **Consistency:** Tunable consistency levels (ONE, QUORUM, ALL)

## Comparison: Same Data, Different Models

### PostgreSQL (Star Schema)
- **1 fact table** + **4 dimension tables**
- JOINs required for most queries
- Foreign key constraints
- ACID transactions

### Cassandra (Query-First)
- **3 denormalized tables**
- No JOINs needed
- Eventual consistency
- Horizontal scalability

**Lesson:** Choose the right tool for the use case!

## Resources

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [DataStax Academy](https://academy.datastax.com/)
- [Cassandra Data Modeling Best Practices](https://www.datastax.com/blog/basic-rules-cassandra-data-modeling)
- [CQL Reference](https://cassandra.apache.org/doc/latest/cql/)

---

**Author:** Sergio Arnold  
**Contact:** sergioarnold87@gmail.com
