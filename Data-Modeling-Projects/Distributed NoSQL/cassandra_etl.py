"""
Cassandra ETL Pipeline for Music Streaming Data
================================================
This script demonstrates query-first data modeling for Apache Cassandra.
Each table is designed to optimize specific query patterns.

Author: Sergio Arnold
"""

import os
import glob
import csv
import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CassandraETL:
    """ETL Pipeline for Cassandra database"""
    
    def __init__(self, contact_points=['127.0.0.1'], keyspace='sparkify'):
        """
        Initialize Cassandra connection
        
        Args:
            contact_points (list): Cassandra cluster contact points
            keyspace (str): Keyspace name
        """
        self.contact_points = contact_points
        self.keyspace = keyspace
        self.cluster = None
        self.session = None
        
    def connect(self):
        """Establish connection to Cassandra cluster"""
        try:
            logger.info(f"Connecting to Cassandra at {self.contact_points}...")
            self.cluster = Cluster(self.contact_points)
            self.session = self.cluster.connect()
            logger.info("Connected successfully!")
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra: {e}")
            raise
    
    def create_keyspace(self, replication_factor=1):
        """
        Create keyspace with replication strategy
        
        Args:
            replication_factor (int): Number of replicas
        """
        try:
            logger.info(f"Creating keyspace '{self.keyspace}'...")
            query = f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH REPLICATION = {{
                    'class': 'SimpleStrategy',
                    'replication_factor': {replication_factor}
                }}
            """
            self.session.execute(query)
            self.session.set_keyspace(self.keyspace)
            logger.info(f"Keyspace '{self.keyspace}' ready!")
        except Exception as e:
            logger.error(f"Failed to create keyspace: {e}")
            raise
    
    def create_tables(self):
        """
        Create tables optimized for specific queries.
        Following Cassandra's query-first modeling approach.
        """
        logger.info("Creating tables...")
        
        # Table 1: Query sessions by sessionId and itemInSession
        # Query: Get artist, song title, and length for sessionId=338, itemInSession=4
        query1 = """
            CREATE TABLE IF NOT EXISTS session_songs (
                session_id INT,
                item_in_session INT,
                artist TEXT,
                song_title TEXT,
                song_length FLOAT,
                PRIMARY KEY (session_id, item_in_session)
            )
        """
        
        # Table 2: Query user activity by userId and sessionId
        # Query: Get artist, song, and user info for userId=10, sessionId=182
        query2 = """
            CREATE TABLE IF NOT EXISTS user_songs (
                user_id INT,
                session_id INT,
                item_in_session INT,
                artist TEXT,
                song TEXT,
                first_name TEXT,
                last_name TEXT,
                PRIMARY KEY ((user_id, session_id), item_in_session)
            )
            WITH CLUSTERING ORDER BY (item_in_session DESC)
        """
        
        # Table 3: Query users by song
        # Query: Get all users who listened to 'All Hands Against His Own'
        query3 = """
            CREATE TABLE IF NOT EXISTS song_users (
                song TEXT,
                user_id INT,
                first_name TEXT,
                last_name TEXT,
                PRIMARY KEY (song, user_id)
            )
        """
        
        try:
            self.session.execute(query1)
            self.session.execute(query2)
            self.session.execute(query3)
            logger.info("Tables created successfully!")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def preprocess_data(self, event_data_path='event_data'):
        """
        Preprocess event CSV files into a single denormalized file
        
        Args:
            event_data_path (str): Path to event data directory
            
        Returns:
            str: Path to processed CSV file
        """
        logger.info("Preprocessing event data files...")
        
        # Get all CSV files
        file_path_list = []
        for root, dirs, files in os.walk(event_data_path):
            file_path_list.extend(glob.glob(os.path.join(root, '*.csv')))
        
        logger.info(f"Found {len(file_path_list)} files to process")
        
        # Combine all files
        full_data_rows_list = []
        for f in file_path_list:
            with open(f, 'r', encoding='utf8', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header
                for line in csvreader:
                    full_data_rows_list.append(line)
        
        # Write combined data
        output_file = 'event_datafile_new.csv'
        csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        
        with open(output_file, 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f, dialect='myDialect')
            writer.writerow([
                'artist', 'firstName', 'gender', 'itemInSession', 'lastName',
                'length', 'level', 'location', 'sessionId', 'song', 'userId'
            ])
            for row in full_data_rows_list:
                if row[0] == '':
                    continue
                writer.writerow((
                    row[0], row[2], row[3], row[4], row[5], row[6],
                    row[7], row[8], row[12], row[13], row[16]
                ))
        
        logger.info(f"Preprocessed data saved to {output_file}")
        return output_file
    
    def load_data(self, csv_file='event_datafile_new.csv'):
        """
        Load data from CSV into Cassandra tables
        
        Args:
            csv_file (str): Path to CSV file
        """
        logger.info(f"Loading data from {csv_file}...")
        
        insert_queries = {
            'session_songs': """
                INSERT INTO session_songs (session_id, item_in_session, artist, song_title, song_length)
                VALUES (%s, %s, %s, %s, %s)
            """,
            'user_songs': """
                INSERT INTO user_songs (user_id, session_id, item_in_session, artist, song, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            'song_users': """
                INSERT INTO song_users (song, user_id, first_name, last_name)
                VALUES (%s, %s, %s, %s)
            """
        }
        
        row_count = 0
        with open(csv_file, encoding='utf8') as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Skip header
            
            for line in csvreader:
                artist, first_name, gender, item_in_session, last_name, \
                length, level, location, session_id, song, user_id = line
                
                # Insert into session_songs
                self.session.execute(
                    insert_queries['session_songs'],
                    (int(session_id), int(item_in_session), artist, song, float(length))
                )
                
                # Insert into user_songs
                self.session.execute(
                    insert_queries['user_songs'],
                    (int(user_id), int(session_id), int(item_in_session),
                     artist, song, first_name, last_name)
                )
                
                # Insert into song_users
                self.session.execute(
                    insert_queries['song_users'],
                    (song, int(user_id), first_name, last_name)
                )
                
                row_count += 1
        
        logger.info(f"Loaded {row_count} rows into all tables")
    
    def run_sample_queries(self):
        """Execute sample queries to demonstrate query patterns"""
        logger.info("\n" + "="*60)
        logger.info("Running sample queries...")
        logger.info("="*60)
        
        # Query 1: Session songs
        logger.info("\nQuery 1: Artist, song, length for sessionId=338, itemInSession=4")
        query1 = """
            SELECT artist, song_title, song_length
            FROM session_songs
            WHERE session_id = 338 AND item_in_session = 4
        """
        rows = self.session.execute(query1)
        for row in rows:
            logger.info(f"  {row.artist} | {row.song_title} | {row.song_length}")
        
        # Query 2: User songs
        logger.info("\nQuery 2: Songs for userId=10, sessionId=182 (sorted by itemInSession)")
        query2 = """
            SELECT item_in_session, artist, song, first_name, last_name
            FROM user_songs
            WHERE user_id = 10 AND session_id = 182
        """
        rows = self.session.execute(query2)
        for row in rows:
            logger.info(f"  {row.item_in_session} | {row.artist} | {row.song} | "
                       f"{row.first_name} {row.last_name}")
        
        # Query 3: Song users
        logger.info("\nQuery 3: Users who listened to 'All Hands Against His Own'")
        query3 = """
            SELECT first_name, last_name
            FROM song_users
            WHERE song = 'All Hands Against His Own'
        """
        rows = self.session.execute(query3)
        for row in rows:
            logger.info(f"  {row.first_name} {row.last_name}")
        
        logger.info("="*60 + "\n")
    
    def drop_tables(self):
        """Drop all tables"""
        logger.info("Dropping tables...")
        self.session.execute("DROP TABLE IF EXISTS session_songs")
        self.session.execute("DROP TABLE IF EXISTS user_songs")
        self.session.execute("DROP TABLE IF EXISTS song_users")
        logger.info("Tables dropped")
    
    def close(self):
        """Close Cassandra connection"""
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
        logger.info("Connection closed")


def main():
    """Main ETL pipeline execution"""
    etl = CassandraETL(contact_points=['127.0.0.1'], keyspace='sparkify')
    
    try:
        # Connect and setup
        etl.connect()
        etl.create_keyspace()
        etl.create_tables()
        
        # Process data
        csv_file = etl.preprocess_data()
        etl.load_data(csv_file)
        
        # Run sample queries
        etl.run_sample_queries()
        
        logger.info("ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise
    finally:
        etl.close()


if __name__ == "__main__":
    main()
