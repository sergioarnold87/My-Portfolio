import psycopg2
import os
import logging
from sql_queries import create_table_queries, drop_table_queries, create_index_queries

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_database():
    """
    Creates and connects to the sparkifydb.
    Uses environment variables for database credentials.
    
    Returns:
        tuple: (cursor, connection) to sparkifydb
    """
    # Get database credentials from environment variables with defaults
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_name = os.getenv('DB_NAME', 'sparkifydb')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'admin')
    default_db = os.getenv('DEFAULT_DB', 'studentdb')
    
    try:
        # Connect to default database
        logger.info(f"Connecting to {db_host} default database...")
        conn = psycopg2.connect(f"host={db_host} dbname={default_db} user={db_user} password={db_password}")
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        
        # Create sparkify database with UTF8 encoding
        logger.info(f"Creating database {db_name}...")
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'utf8' TEMPLATE template0")
        
        # Close connection to default database
        conn.close()
        
        # Connect to sparkify database
        logger.info(f"Connecting to {db_name} database...")
        conn = psycopg2.connect(f"host={db_host} dbname={db_name} user={db_user} password={db_password}")
        cur = conn.cursor()
        
        return cur, conn
    
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    
    Args:
        cur: Database cursor
        conn: Database connection
    """
    logger.info("Dropping existing tables...")
    for query in drop_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error dropping table: {e}")
            raise


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    
    Args:
        cur: Database cursor
        conn: Database connection
    """
    logger.info("Creating tables...")
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error creating table: {e}")
            raise


def create_indexes(cur, conn):
    """
    Creates indexes using the queries in `create_index_queries` list.
    
    Args:
        cur: Database cursor
        conn: Database connection
    """
    logger.info("Creating indexes for query optimization...")
    for query in create_index_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error creating index: {e}")
            raise


def main():
    """
    Main function to set up the Sparkify database.
    
    Steps:
    1. Drops (if exists) and creates the sparkify database
    2. Establishes connection with the sparkify database
    3. Drops all existing tables
    4. Creates all tables needed
    5. Creates indexes for performance optimization
    6. Closes the connection
    """
    try:
        cur, conn = create_database()
        
        drop_tables(cur, conn)
        create_tables(cur, conn)
        create_indexes(cur, conn)
        
        logger.info("Database setup completed successfully!")
        conn.close()
        
    except Exception as e:
        logger.error(f"Failed to set up database: {e}")
        raise


if __name__ == "__main__":
    main()
