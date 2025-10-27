# Sparkify Data Modeling Project - PostgreSQL

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

## Project Overview

A production-ready **Star Schema** data warehouse implementation for Sparkify, a music streaming application. This project demonstrates professional-level **relational database modeling** using PostgreSQL, featuring optimized ETL pipelines, comprehensive indexing strategies, and ACID compliance for analytical workloads.

### Key Features

✅ **Star Schema Design** - Optimized for OLAP queries  
✅ **Foreign Key Constraints** - Ensures referential integrity  
✅ **Strategic Indexing** - 9 indexes for query performance  
✅ **Environment-based Configuration** - Secure credential management  
✅ **Comprehensive Logging** - Full ETL observability  
✅ **Error Handling** - Robust exception management  
✅ **ON CONFLICT Handling** - Upsert operations for data consistency

## Project Structure

- **create_tables.py:** Python script to create database tables based on the schema defined in `sql_queries.py`.
- **etl.py:** Python script to extract, transform, and load data from JSON files into the PostgreSQL database.
- **sql_queries.py:** Contains SQL queries to create tables, insert data, and perform analytical operations.
- **data/:** Directory containing sample JSON data files for song and log data.

## Database Schema

### Star Schema Architecture

The database implements a **Star Schema** optimized for analytical queries:

```
                    ┌─────────────┐
                    │   users     │
                    │ (DIMENSION) │
                    └──────┬──────┘
                           │
       ┌─────────────┐     │     ┌─────────────┐
       │   songs     │─────┼─────│   artists   │
       │ (DIMENSION) │     │     │ (DIMENSION) │
       └──────┬──────┘     │     └──────┬──────┘
              │            │            │
              │     ┌──────▼──────┐     │
              └─────►  songplays  ◄─────┘
                    │   (FACT)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    time     │
                    │ (DIMENSION) │
                    └─────────────┘
```

### Fact Table

#### `songplays` - User song play events
| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| songplay_id | SERIAL | Primary key | PRIMARY KEY |
| start_time | TIMESTAMP | Event timestamp | FOREIGN KEY → time(start_time) |
| user_id | INT | User identifier | NOT NULL, FOREIGN KEY → users(user_id) |
| level | TEXT | Subscription level | |
| song_id | TEXT | Song identifier | FOREIGN KEY → songs(song_id) |
| artist_id | TEXT | Artist identifier | FOREIGN KEY → artists(artist_id) |
| session_id | INT | Session identifier | |
| location | TEXT | User location | |
| user_agent | TEXT | User's device info | |

### Dimension Tables

#### `users` - User information
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | INT | PRIMARY KEY |
| first_name | TEXT | NOT NULL |
| last_name | TEXT | NOT NULL |
| gender | TEXT | |
| level | TEXT | |

#### `songs` - Song catalog
| Column | Type | Constraints |
|--------|------|-------------|
| song_id | TEXT | PRIMARY KEY |
| title | TEXT | NOT NULL |
| artist_id | TEXT | NOT NULL |
| year | INT | |
| duration | FLOAT | NOT NULL |

#### `artists` - Artist catalog
| Column | Type | Constraints |
|--------|------|-------------|
| artist_id | TEXT | PRIMARY KEY |
| name | TEXT | NOT NULL |
| location | TEXT | |
| latitude | FLOAT | |
| longitude | FLOAT | |

#### `time` - Time dimension for temporal analysis
| Column | Type | Constraints |
|--------|------|-------------|
| start_time | TIMESTAMP | PRIMARY KEY |
| hour | INT | |
| day | INT | |
| week | INT | |
| month | INT | |
| year | INT | |
| weekday | TEXT | |

### Performance Optimization

**9 Strategic Indexes** created for query acceleration:
- `idx_users_level` - User subscription analysis
- `idx_songs_artist` - Song-artist joins
- `idx_artists_name` - Artist name searches
- `idx_time_year`, `idx_time_month` - Temporal filtering
- `idx_songplays_user` - User activity queries
- `idx_songplays_song` - Song popularity analysis
- `idx_songplays_artist` - Artist analytics
- `idx_songplays_time` - Time-based analysis

## Installation & Setup

### Prerequisites

- **PostgreSQL 13+** - [Installation Guide](https://www.postgresql.org/download/)
- **Python 3.8+**
- **pip** package manager

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Data-Modeling-Projects/Relational-DataBase
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Credentials

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```ini
DB_HOST=127.0.0.1
DB_NAME=sparkifydb
DB_USER=your_username
DB_PASSWORD=your_password
DEFAULT_DB=postgres
```

### Step 5: Create Database Schema

```bash
python create_tables.py
```

This will:
- Create the `sparkifydb` database
- Create all fact and dimension tables
- Create performance indexes
- Set up foreign key constraints

### Step 6: Run ETL Pipeline

```bash
python etl.py
```

This will:
- Extract data from `data/song_data` and `data/log_data`
- Transform and clean the data
- Load into PostgreSQL tables

## Usage Examples

### Query 1: Top 10 Most Played Songs

```sql
SELECT 
    s.title,
    a.name AS artist,
    COUNT(*) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
JOIN artists a ON sp.artist_id = a.artist_id
GROUP BY s.title, a.name
ORDER BY play_count DESC
LIMIT 10;
```

### Query 2: User Activity by Hour

```sql
SELECT 
    t.hour,
    COUNT(*) AS plays
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.hour
ORDER BY t.hour;
```

### Query 3: Free vs Paid User Analysis

```sql
SELECT 
    level,
    COUNT(DISTINCT user_id) AS user_count,
    COUNT(*) AS total_plays,
    AVG(COUNT(*)) OVER (PARTITION BY level) AS avg_plays_per_user
FROM songplays
GROUP BY level;
```

## Data Model Highlights

### Why Star Schema?

1. **Query Performance** - Denormalized structure minimizes JOINs
2. **Business Intelligence** - Intuitive for BI tools and analysts
3. **Scalability** - Easy to add new dimensions
4. **Aggregation Speed** - Optimized for SUM, COUNT, AVG operations

### Design Decisions

- **SERIAL for songplay_id** - Auto-incrementing primary key for fact table
- **TIMESTAMP for time dimension** - Precise temporal analysis
- **ON CONFLICT handling** - Prevents duplicate dimension entries
- **Foreign keys** - Enforces referential integrity
- **Strategic indexes** - Covers common query patterns

## File Structure

```
Relational-DataBase/
├── create_tables.py        # Database & table creation
├── etl.py                  # ETL pipeline
├── sql_queries.py          # SQL DDL & DML statements
├── test.ipynb              # Query testing notebook
├── etl.ipynb               # ETL development notebook
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── readme.md               # This file
└── Data/                   # Sample JSON data
    ├── song_data/
    └── log_data/
```

## Technologies Used

- **PostgreSQL** - Relational database
- **Python 3.8+** - ETL scripting
- **psycopg2** - PostgreSQL adapter
- **Pandas** - Data transformation
- **python-dotenv** - Environment management

## Best Practices Demonstrated

✅ Environment-based configuration  
✅ Comprehensive error handling  
✅ Structured logging  
✅ Foreign key constraints  
✅ Indexed query optimization  
✅ ACID compliance  
✅ Upsert operations (ON CONFLICT)  
✅ Type safety and validation

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Star Schema Design](https://en.wikipedia.org/wiki/Star_schema)
- [Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [psycopg2 Guide](https://www.psycopg.org/docs/)

---

**Author:** Sergio Arnold  
**Contact:** sergioarnold87@gmail.com

