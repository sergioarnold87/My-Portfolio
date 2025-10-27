# Cassandra Data Model - Detailed Documentation

## Query-First Modeling Approach

In Cassandra, **we design tables around queries, not entities**. Each query gets its own optimized table.

---

## Query Patterns & Table Designs

### Query 1: Session-Based Song Lookup

**Business Question:** "What song was played at a specific point in a user's session?"

**Access Pattern:**
```sql
SELECT artist, song_title, song_length
FROM session_songs
WHERE session_id = 338 AND item_in_session = 4;
```

#### Table 1: `session_songs`

```
┌─────────────────────────────────────────────────────────────┐
│                      session_songs                          │
├─────────────────────────────────────────────────────────────┤
│ PARTITION KEY    session_id         INT                     │
│ CLUSTERING KEY   item_in_session    INT                     │
│                  artist             TEXT                    │
│                  song_title         TEXT                    │
│                  song_length        FLOAT                   │
└─────────────────────────────────────────────────────────────┘

PRIMARY KEY (session_id, item_in_session)
               └─ Partition    └─ Clustering (sort order)
```

**Why This Design?**

✅ **Partition Key = session_id**
- All songs in a session stored together on same node
- Fast lookup by session
- Natural data locality

✅ **Clustering Key = item_in_session**
- Songs sorted by playback order within partition
- Efficient range queries (get all songs in session)
- Chronological ordering maintained

**Data Distribution:**
```
Node 1: session_id = 23, 456, 789, ...
Node 2: session_id = 101, 234, 567, ...
Node 3: session_id = 338, 401, 512, ...
         └─ This partition contains all items for session 338
```

**Query Performance:**
- **Lookup:** O(1) - Single partition read
- **Latency:** <5ms typical
- **Scalability:** Distributes evenly across cluster

---

### Query 2: User Session Activity

**Business Question:** "What songs did a specific user play in a given session?"

**Access Pattern:**
```sql
SELECT artist, song, first_name, last_name
FROM user_songs
WHERE user_id = 10 AND session_id = 182
ORDER BY item_in_session DESC;
```

#### Table 2: `user_songs`

```
┌─────────────────────────────────────────────────────────────┐
│                      user_songs                             │
├─────────────────────────────────────────────────────────────┤
│ PARTITION KEY    (user_id, session_id)  INT, INT           │
│ CLUSTERING KEY   item_in_session        INT (DESC)         │
│                  artist                  TEXT               │
│                  song                    TEXT               │
│                  first_name              TEXT               │
│                  last_name               TEXT               │
└─────────────────────────────────────────────────────────────┘

PRIMARY KEY ((user_id, session_id), item_in_session)
              └─ Composite Partition    └─ Clustering (DESC)

WITH CLUSTERING ORDER BY (item_in_session DESC)
```

**Why This Design?**

✅ **Composite Partition Key = (user_id, session_id)**
- Unique partition per user session
- Prevents hot spots (single user's sessions distributed)
- Natural query boundary

✅ **Clustering Key = item_in_session DESC**
- Most recent plays first
- Descending order for recency queries
- Sorted within partition

✅ **Denormalization**
- User data (first_name, last_name) duplicated
- Eliminates need for JOINs
- Disk space traded for query speed

**Data Distribution:**
```
Partition Key Hash
├─ (user_id=10, session_id=182) → Node 1
├─ (user_id=10, session_id=183) → Node 3  ← Different partition!
├─ (user_id=11, session_id=182) → Node 2
└─ (user_id=12, session_id=182) → Node 1
```

**Query Performance:**
- **Lookup:** O(1) - Single partition read
- **Sort:** Pre-sorted by clustering key (no sort needed!)
- **Latency:** <5ms typical

---

### Query 3: Song Popularity Analysis

**Business Question:** "Which users have listened to a specific song?"

**Access Pattern:**
```sql
SELECT first_name, last_name
FROM song_users
WHERE song = 'All Hands Against His Own';
```

#### Table 3: `song_users`

```
┌─────────────────────────────────────────────────────────────┐
│                      song_users                             │
├─────────────────────────────────────────────────────────────┤
│ PARTITION KEY    song         TEXT                          │
│ CLUSTERING KEY   user_id      INT                           │
│                  first_name   TEXT                          │
│                  last_name    TEXT                          │
└─────────────────────────────────────────────────────────────┘

PRIMARY KEY (song, user_id)
              └─ Partition  └─ Clustering (ensures uniqueness)
```

**Why This Design?**

✅ **Partition Key = song**
- All listeners of a song stored together
- Supports song popularity queries
- Natural grouping for analytics

✅ **Clustering Key = user_id**
- Ensures unique users per song
- Sorted by user_id within partition
- Prevents duplicate entries

✅ **Denormalization**
- User names duplicated from user dimension
- No JOINs needed for user info
- Complete data in single query

**Potential Hot Partition Warning:**
```
Popular song → Large partition → Possible performance issue
Solution: Add time bucket to partition key if needed
  PRIMARY KEY ((song, time_bucket), user_id)
```

**Query Performance:**
- **Lookup:** O(1) - Single partition read
- **Latency:** <10ms (depends on partition size)
- **Scalability:** Popular songs may need partition splitting

---

## Data Denormalization Examples

### Example 1: User Data Duplication

**In user_songs table:**
```
user_id | session_id | first_name | last_name | ...
--------|------------|------------|-----------|----
   10   |    182     |  Sylvie    |   Cruz    | ...
   10   |    183     |  Sylvie    |   Cruz    | ... ← Duplicated!
```

**Why?**
- ❌ Cassandra doesn't support JOINs
- ✅ Single query gets all needed data
- ✅ Disk space is cheap, JOINs are expensive

### Example 2: Song Title Duplication

**In session_songs:**
```
session_id | song_title              | artist     | ...
-----------|-------------------------|------------|----
    338    | Music Matters (Dub)     | Faithless  | ...
```

**In user_songs:**
```
user_id | song                    | artist     | ...
--------|-------------------------|------------|----
   10   | Music Matters (Dub)     | Faithless  | ... ← Same song!
```

**Trade-off:**
- ❌ Data duplicated across tables
- ✅ Each query optimized independently
- ✅ No cross-table dependencies

---

## Partition Key Design Principles

### 1. Single Partition Key
**Example:** `session_id`

**Characteristics:**
- Simple, single-column partition key
- Data distributed by hash of session_id
- All items with same session_id on same node

**When to Use:**
- Natural grouping exists
- Partition size bounded
- Even distribution expected

### 2. Composite Partition Key
**Example:** `(user_id, session_id)`

**Characteristics:**
- Multi-column partition key
- Data distributed by hash of both columns
- More granular partitioning

**When to Use:**
- Prevent hot spots
- Finer-grained distribution
- Limit partition size

### 3. Partition Size Considerations

**Good Partition:**
- Size: <100MB
- Rows: <100,000
- Read latency: <10ms

**Bad Partition (Hot Partition):**
- Size: >100MB
- Rows: >100,000
- Read latency: >50ms
- **Fix:** Add time bucket to partition key

---

## Clustering Key Design Principles

### Ascending Order (Default)
```sql
PRIMARY KEY (partition_key, clustering_key)
-- clustering_key sorted: 1, 2, 3, 4, ...
```

**Use Case:** Chronological data (oldest first)

### Descending Order
```sql
PRIMARY KEY ((user_id, session_id), item_in_session)
WITH CLUSTERING ORDER BY (item_in_session DESC)
-- item_in_session sorted: 10, 9, 8, 7, ...
```

**Use Case:** Recent data first (leaderboards, activity feeds)

### Multiple Clustering Keys
```sql
PRIMARY KEY (partition_key, clustering_key1, clustering_key2)
-- Sorted by clustering_key1, then clustering_key2
```

**Use Case:** Multi-level sorting (year, month, day)

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Secondary Indexes
```sql
-- DON'T DO THIS
CREATE INDEX ON session_songs (artist);

-- Instead, create a new table:
CREATE TABLE songs_by_artist (
    artist TEXT,
    session_id INT,
    song_title TEXT,
    PRIMARY KEY (artist, session_id)
);
```

**Why?**
- Secondary indexes are slow in Cassandra
- Queries scan entire cluster
- Use denormalized tables instead

### ❌ Anti-Pattern 2: ALLOW FILTERING
```sql
-- DON'T DO THIS
SELECT * FROM session_songs 
WHERE artist = 'Faithless' 
ALLOW FILTERING;

-- This scans entire table!
```

**Why?**
- Forces full table scan
- Terrible performance at scale
- Design table for this query instead

### ❌ Anti-Pattern 3: Unbounded Partitions
```sql
-- RISKY DESIGN
PRIMARY KEY (user_id, timestamp)

-- If one user has millions of events, partition becomes huge
-- Better: Add time bucket
PRIMARY KEY ((user_id, time_bucket), timestamp)
```

---

## Replication & Consistency

### Replication Factor
```sql
CREATE KEYSPACE sparkify
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3  ← Data replicated 3 times
};
```

**Production Recommendation:**
- **RF = 3** (Standard for production)
- Tolerates 2 node failures
- Balance between durability and cost

### Consistency Levels

**Write Consistency:**
```python
session.execute(query, consistency_level=ConsistencyLevel.QUORUM)
# QUORUM = majority of replicas must acknowledge
# For RF=3: Need 2 acknowledgments
```

**Read Consistency:**
```python
session.execute(query, consistency_level=ConsistencyLevel.ONE)
# ONE = Read from nearest replica (fastest)
# QUORUM = Read from majority (stronger consistency)
```

**CAP Theorem Trade-offs:**
- **ONE:** Low latency, eventual consistency
- **QUORUM:** Balanced latency and consistency
- **ALL:** Strong consistency, high latency

---

## Performance Optimization Tips

### 1. Batch Inserts
```python
from cassandra.query import BatchStatement

batch = BatchStatement()
for row in data:
    batch.add(insert_query, row)
session.execute(batch)
```

**Benefits:**
- Fewer network round trips
- Better throughput
- Atomic within partition

### 2. Prepared Statements
```python
prepared = session.prepare("""
    INSERT INTO session_songs (session_id, item_in_session, artist, song_title, song_length)
    VALUES (?, ?, ?, ?, ?)
""")

session.execute(prepared, (session_id, item, artist, song, length))
```

**Benefits:**
- Query parsed once
- 10-20% performance improvement
- Reduced CPU usage

### 3. Async Queries
```python
from cassandra.concurrent import execute_concurrent_with_args

execute_concurrent_with_args(session, prepared, data, concurrency=50)
```

**Benefits:**
- Parallel execution
- Higher throughput
- Better resource utilization

---

## Comparison: PostgreSQL vs Cassandra

### Same Query, Different Approach

#### PostgreSQL (JOINs)
```sql
-- Multiple tables, JOINs required
SELECT 
    s.title,
    a.name AS artist,
    u.first_name,
    u.last_name
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
JOIN artists a ON sp.artist_id = a.artist_id
JOIN users u ON sp.user_id = u.user_id
WHERE sp.session_id = 338 AND sp.item_in_session = 4;
```

**Performance:**
- 4 table JOINs
- Index lookups required
- ~10-50ms latency

#### Cassandra (Denormalized)
```sql
-- Single table, no JOINs
SELECT artist, song_title, first_name, last_name
FROM session_songs
WHERE session_id = 338 AND item_in_session = 4;
```

**Performance:**
- Single partition read
- No JOINs needed
- ~5ms latency

---

## Maintenance & Operations

### Compaction Strategy
```sql
ALTER TABLE session_songs 
WITH compaction = {
    'class': 'SizeTieredCompactionStrategy'
};
```

**Strategies:**
- **SizeTiered:** General purpose, write-heavy
- **Leveled:** Read-heavy, predictable latency
- **TimeWindow:** Time-series data

### Repair Operations
```bash
# Repair data across replicas
nodetool repair sparkify session_songs

# Run weekly for consistency
```

### Monitoring
```bash
# Check table statistics
nodetool cfstats sparkify.session_songs

# Monitor partition sizes
nodetool cfhistograms sparkify session_songs
```

---

**Author:** Sergio Arnold  
**Last Updated:** 2024  
**Version:** 1.0
