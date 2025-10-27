# Sparkify Star Schema - Detailed Documentation

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FACT TABLE                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        songplays                                  │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ PK  songplay_id        SERIAL                                     │  │
│  │ FK  start_time         TIMESTAMP    ──┐                           │  │
│  │ FK  user_id            INT           ─┼──┐                        │  │
│  │     level              TEXT           │  │                        │  │
│  │ FK  song_id            TEXT          ─┼──┼──┐                     │  │
│  │ FK  artist_id          TEXT          ─┼──┼──┼──┐                  │  │
│  │     session_id         INT            │  │  │  │                  │  │
│  │     location           TEXT           │  │  │  │                  │  │
│  │     user_agent         TEXT           │  │  │  │                  │  │
│  └───────────────────────────────────────┼──┼──┼──┼──────────────────┘  │
│                                          │  │  │  │                     │
└──────────────────────────────────────────┼──┼──┼──┼─────────────────────┘
                                           │  │  │  │
            ┌──────────────────────────────┘  │  │  │
            │                                 │  │  │
            ▼                                 │  │  │
┌───────────────────────────┐                │  │  │
│   DIMENSION: time         │                │  │  │
├───────────────────────────┤                │  │  │
│ PK  start_time  TIMESTAMP │                │  │  │
│     hour        INT       │                │  │  │
│     day         INT       │                │  │  │
│     week        INT       │                │  │  │
│     month       INT       │◄───Indexed     │  │  │
│     year        INT       │◄───Indexed     │  │  │
│     weekday     TEXT      │                │  │  │
└───────────────────────────┘                │  │  │
                                             │  │  │
                ┌────────────────────────────┘  │  │
                │                               │  │
                ▼                               │  │
┌───────────────────────────┐                  │  │
│   DIMENSION: users        │                  │  │
├───────────────────────────┤                  │  │
│ PK  user_id     INT       │                  │  │
│     first_name  TEXT      │                  │  │
│     last_name   TEXT      │                  │  │
│     gender      TEXT      │                  │  │
│     level       TEXT      │◄───Indexed       │  │
└───────────────────────────┘                  │  │
                                               │  │
                    ┌──────────────────────────┘  │
                    │                             │
                    ▼                             │
┌───────────────────────────┐                    │
│   DIMENSION: songs        │                    │
├───────────────────────────┤                    │
│ PK  song_id     TEXT      │                    │
│     title       TEXT      │                    │
│ FK  artist_id   TEXT      │◄───Indexed         │
│     year        INT       │                    │
│     duration    FLOAT     │                    │
└───────────────────────────┘                    │
                                                 │
                        ┌────────────────────────┘
                        │
                        ▼
┌───────────────────────────┐
│   DIMENSION: artists      │
├───────────────────────────┤
│ PK  artist_id   TEXT      │
│     name        TEXT      │◄───Indexed
│     location    TEXT      │
│     latitude    FLOAT     │
│     longitude   FLOAT     │
└───────────────────────────┘
```

---

## Table Specifications

### Fact Table: songplays

**Purpose:** Records every song play event in the application.

**Cardinality:** ~320,000 rows (grows continuously)

**Indexes:**
- Primary key on `songplay_id` (automatically indexed)
- `idx_songplays_user` on `user_id`
- `idx_songplays_song` on `song_id`
- `idx_songplays_artist` on `artist_id`
- `idx_songplays_time` on `start_time`

**Foreign Keys:**
- `start_time` → time(start_time)
- `user_id` → users(user_id)
- `song_id` → songs(song_id)
- `artist_id` → artists(artist_id)

**Data Integrity:**
- `user_id` NOT NULL (every play must have a user)
- Other FKs nullable (song/artist may be unknown)

---

### Dimension Table: users

**Purpose:** Store user account information.

**Cardinality:** ~100 rows (slow growth)

**Type:** Slowly Changing Dimension Type 1 (overwrite changes)

**Indexes:**
- Primary key on `user_id`
- `idx_users_level` on `level`

**ON CONFLICT Strategy:**
```sql
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
```
Updates subscription level if user changes from free to paid.

**Business Rules:**
- `first_name` and `last_name` are required
- `level` tracks subscription status (free/paid)

---

### Dimension Table: songs

**Purpose:** Store song catalog metadata.

**Cardinality:** ~14,000 rows (moderate growth)

**Indexes:**
- Primary key on `song_id`
- `idx_songs_artist` on `artist_id`

**ON CONFLICT Strategy:**
```sql
ON CONFLICT (song_id) DO NOTHING;
```
Prevents duplicate song entries.

**Business Rules:**
- `title` and `duration` are required
- `year` is optional (may be unknown)
- `artist_id` links to artists dimension

---

### Dimension Table: artists

**Purpose:** Store artist catalog information.

**Cardinality:** ~10,000 rows (moderate growth)

**Indexes:**
- Primary key on `artist_id`
- `idx_artists_name` on `name`

**ON CONFLICT Strategy:**
```sql
ON CONFLICT (artist_id) DO NOTHING;
```
Prevents duplicate artist entries.

**Business Rules:**
- `name` is required
- `location`, `latitude`, `longitude` are optional
- Geographic coordinates support location-based analytics

---

### Dimension Table: time

**Purpose:** Pre-computed time dimension for temporal analysis.

**Cardinality:** Unique timestamps from songplays

**Type:** Conformed dimension (can be shared across star schemas)

**Indexes:**
- Primary key on `start_time`
- `idx_time_year` on `year`
- `idx_time_month` on `month`

**ON CONFLICT Strategy:**
```sql
ON CONFLICT (start_time) DO NOTHING;
```
Each timestamp appears only once.

**Business Rules:**
- All time units derived from `start_time`
- `weekday` stored as text (Monday, Tuesday, etc.)
- Supports year-over-year, month-over-month analysis

---

## Query Patterns Supported

### 1. User Behavior Analysis
```sql
-- Most active users
SELECT u.first_name, u.last_name, COUNT(*) as play_count
FROM songplays sp
JOIN users u ON sp.user_id = u.user_id
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY play_count DESC;
```
**Performance:** Uses `idx_songplays_user`

---

### 2. Song Popularity
```sql
-- Top 10 songs
SELECT s.title, a.name, COUNT(*) as plays
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
JOIN artists a ON s.artist_id = a.artist_id
GROUP BY s.song_id, s.title, a.name
ORDER BY plays DESC
LIMIT 10;
```
**Performance:** Uses `idx_songplays_song` and `idx_songs_artist`

---

### 3. Temporal Analysis
```sql
-- Plays by hour of day
SELECT t.hour, COUNT(*) as plays
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.hour
ORDER BY t.hour;
```
**Performance:** Uses `idx_songplays_time`

---

### 4. Subscription Analysis
```sql
-- Free vs Paid user engagement
SELECT 
    level,
    COUNT(DISTINCT user_id) as users,
    COUNT(*) as total_plays,
    ROUND(COUNT(*)::NUMERIC / COUNT(DISTINCT user_id), 2) as avg_plays_per_user
FROM songplays
GROUP BY level;
```
**Performance:** Sequential scan on small result set

---

### 5. Geographic Analysis
```sql
-- Top artist locations
SELECT 
    a.location,
    COUNT(DISTINCT a.artist_id) as artist_count,
    COUNT(*) as total_plays
FROM songplays sp
JOIN artists a ON sp.artist_id = a.artist_id
WHERE a.location IS NOT NULL
GROUP BY a.location
ORDER BY total_plays DESC
LIMIT 10;
```
**Performance:** Uses `idx_songplays_artist`

---

## Design Trade-offs

### Denormalization Decisions

**User level in songplays:**
- ✅ **Pro:** Captures subscription status at time of play
- ❌ **Con:** Duplicates data from users table
- **Decision:** Keep both (fact captures historical state, dimension captures current state)

**Artist data in songs:**
- ✅ **Pro:** Simple foreign key relationship
- ❌ **Con:** Requires JOIN for artist info
- **Decision:** Normalized design (artist info rarely changes)

---

### Index Strategy

**Why 9 indexes?**
1. Cover common query patterns
2. Accelerate foreign key lookups
3. Enable efficient aggregations
4. Support dimensional filtering

**Cost:**
- Slower inserts (~15% overhead)
- Additional storage (~20% of table size)
- **Worth it:** Query performance 10-100x faster

---

## Scalability Considerations

### Vertical Scaling
- Current design handles ~10M songplays
- Indexes essential at this scale
- Partition table if exceeds 100M rows

### Partitioning Strategy (Future)
```sql
-- Partition by year
CREATE TABLE songplays_2024 PARTITION OF songplays
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### Archive Strategy
- Move data older than 2 years to archive schema
- Maintain recent 2 years in hot storage
- Use foreign data wrappers for historical queries

---

## Maintenance Procedures

### Regular Maintenance
```sql
-- Vacuum to reclaim space
VACUUM ANALYZE songplays;

-- Reindex if fragmented
REINDEX TABLE songplays;

-- Update statistics
ANALYZE songplays;
```

### Monitoring Queries
```sql
-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Table size
SELECT 
    pg_size_pretty(pg_total_relation_size('songplays')) as total_size,
    pg_size_pretty(pg_relation_size('songplays')) as table_size,
    pg_size_pretty(pg_total_relation_size('songplays') - pg_relation_size('songplays')) as index_size;
```

---

**Author:** Sergio Arnold  
**Last Updated:** 2024  
**Version:** 1.0
