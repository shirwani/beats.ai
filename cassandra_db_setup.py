from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'], port=9042, connect_timeout=10)
session = cluster.connect('beats_ai')


def create_db_table():
    query = """
        CREATE TABLE IF NOT EXISTS TRACKS (
            id              TEXT PRIMARY KEY,
            title           TEXT,
            artist          TEXT,
            genre           TEXT,
            url             TEXT,
            filename        TEXT,
            views           INT,
            likes           INT,
            tempo           FLOAT,
            energy          FLOAT,
            danceability    FLOAT,
            complexity      FLOAT,
            speechiness     FLOAT,
            loudness        FLOAT,
            valence         FLOAT,
            time_signature  FLOAT,
            key             INT,
            key_mode        INT
        );       
    """
    session.execute(query)


if __name__ == '__main__':
    create_db_table()
    cluster.shutdown()