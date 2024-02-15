# Sparkify Data Modeling Project

## Project Overview

Welcome to the Sparkify Data Modeling Project! This project focuses on designing and implementing a database schema for Sparkify, a music streaming application. The goal is to create an efficient database structure that can store and manage user activity, song metadata, and other relevant data to support analytical queries.

## Project Structure

- **create_tables.py:** Python script to create database tables based on the schema defined in `sql_queries.py`.
- **etl.py:** Python script to extract, transform, and load data from JSON files into the PostgreSQL database.
- **sql_queries.py:** Contains SQL queries to create tables, insert data, and perform analytical operations.
- **data/:** Directory containing sample JSON data files for song and log data.

## Database Schema

The database schema for Sparkify consists of a star schema with the following tables:

- **Fact Table:**
  - `songplays`: Records of user song plays, including information about the song, user, session, and location.

- **Dimension Tables:**
  - `users`: Information about Sparkify users, including user ID, first name, last name, gender, and level (subscription type).
  - `songs`: Information about songs in the Sparkify database, including song ID, title, artist ID, year, and duration.
  - `artists`: Information about artists in the Sparkify database, including artist ID, name, location, latitude, and longitude.
  - `time`: Timestamp information derived from the `start_time` field in the `songplays` table, broken down into various time units (hour, day, week, month, year, weekday).

## How to Use

1. Ensure you have PostgreSQL installed on your system.
2. Run `create_tables.py` to create the necessary database tables.
3. Run `etl.py` to extract data from JSON files, transform it, and load it into the PostgreSQL database.
4. Use SQL queries from `sql_queries.py` to perform analytical operations on the data.
5. Explore the data and analyze user behavior, song popularity, and other insights to support business decisions.

## Dependencies

- PostgreSQL: Ensure you have PostgreSQL installed and running on your system.
- Python 3.x: Install the required Python dependencies using `pip install -r requirements.txt`.

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python PostgreSQL Tutorial](https://www.postgresqltutorial.com/postgresql-python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

