from cassandra.cluster import Cluster
from utils import *

class Cassandra:
    def __init__(self):
        cfg = read_from_json_file('config.json')
        db_host     = cfg['database']['db_host']
        db_port     = cfg['database']['db_port']
        db_timeout  = cfg['database']['db_timeout']
        db_keyspace = cfg['database']['db_keyspace']

        self.db_tablename = cfg['downloads']['db_tablename']
        self.db_cluster = Cluster([db_host], port=db_port, connect_timeout=db_timeout)
        self.db_session = self.db_cluster.connect(db_keyspace)


    def shutdown(self):
        self.db_cluster.shutdown()


    def create_db_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.db_tablename} (
                id              TEXT PRIMARY KEY,
                title           TEXT,
                artist          TEXT,
                genre           TEXT,
                publisher       TEXT,
                url             TEXT,
                filename        TEXT,
                views           INT,
                likes           INT,
                comments        INT,
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
        self.db_session.execute(query)

    def record_single_track_info(self, track):
        query = f"""
            INSERT INTO {self.db_tablename} (id, artist, title, genre, publisher, url, filename, views, likes, comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            self.db_session.execute(
                query,
                (hashify(f"{track['artist']} - {track['title']}"),
                 track['artist'],
                 track['title'],
                 track['genre'],
                 track['publisher'],
                 track['url'],
                 track['filename'],
                 int(track['views']),
                 int(track['likes']),
                 int(track['comments'])
                 )
            )
        except Exception as e:
            print(f"Query failed: {e}")

    @fcn_logger
    def get_tracks(self, num_tracks=10000):
        query = f"SELECT * FROM {self.db_tablename};"
        tracks = self.db_session.execute(query)

        ptracks = list()
        for track in tracks:
            ptracks.append(track._asdict())

        return ptracks

    @fcn_logger
    def get_unanalyzed_tracks(self, num_tracks=10000):
        query = f"SELECT * FROM {self.db_tablename};"
        tracks = self.db_session.execute(query)

        ptracks = list()
        for track in tracks:
            t = track._asdict()
            if t['complexity'] is not None:
                continue
            ptracks.append(t)

        return ptracks

    @fcn_logger
    def get_track_ids(self, num_tracks=10000):
        query = f"SELECT * FROM {self.db_tablename};"
        tracks = self.db_session.execute(query)

        ptracks = list()
        for track in tracks:
            t = track._asdict()
            ptracks.append(t['id'])

        return ptracks


    @fcn_logger
    def update_db_track_info(self, track, features):
        if True:
            query = f"""
            UPDATE {self.db_tablename} SET
             tempo           = %s,
             energy          = %s,
             danceability    = %s,
             complexity      = %s,
             speechiness     = %s,
             loudness        = %s,
             valence         = %s,
             time_signature  = %s,
             key             = %s,
             key_mode        = %s
            WHERE id = %s;
            """

            self.db_session.execute(query, (
                features['tempo'],
                features['energy'],
                features['danceability'],
                features['complexity'],
                features['speechiness'],
                features['loudness'],
                features['valence'],
                features['time_signature'],
                features['key'],
                features['key_mode'],
                track['id']))

    def get_data_by_row_from_db(self, db_tablename, colname, colval):
        query = f"SELECT * FROM {db_tablename} WHERE {colname} = %s ALLOW FILTERING;"
        tracks = self.db_session.execute(query, (colval, ))

        data = list()
        for track in tracks:
            d = dict()
            d['tempo'] = track.tempo
            d['energy'] = track.energy
            d['danceability'] = track.danceability
            d['complexity'] = track.complexity
            d['speechiness'] = track.speechiness
            d['loudness'] = track.loudness
            d['valence'] = track.valence
            d['time_signature'] = track.time_signature
            d['key'] = track.key
            d['key_mode'] = track.key_mode
            d['views'] = track.views
            d['likes'] = track.likes
            d['popularity'] = track.likes/track.views
            data.append(d)

        return data

    def get_data_from_db(self, db_tablename, colname, colval):
        query = f"SELECT * FROM {db_tablename} WHERE {colname} = %s ALLOW FILTERING;"
        tracks = self.db_session.execute(query, (colval, ))

        data = dict()
        data['tempo'] = list()
        data['energy'] = list()
        data['danceability'] = list()
        data['complexity'] = list()
        data['speechiness'] = list()
        data['loudness'] = list()
        data['valence'] = list()
        data['time_signature'] = list()
        data['key'] = list()
        data['key_mode'] = list()
        data['views'] = list()
        data['likes'] = list()
        data['popularity'] = list()

        for track in tracks:
            data['tempo'].append(track.tempo)
            data['energy'].append(track.energy)
            data['danceability'].append(track.danceability)
            data['complexity'].append(track.complexity)
            data['speechiness'].append(track.speechiness)
            data['loudness'].append(track.loudness)
            data['valence'].append(track.valence)
            data['time_signature'].append(track.time_signature)
            data['key'].append(track.key)
            data['key_mode'].append(track.key_mode)
            data['views'].append(track.views)
            data['likes'].append(track.likes)
            data['popularity'].append(track.likes/track.views)

        return data


    def get_single_item_from_db(self, db_tablename, colname, colval):
        query = f"SELECT * FROM {db_tablename} WHERE {colname} = %s LIMIT 1 ALLOW FILTERING;"
        tracks = self.db_session.execute(query, (colval, ))

        data = dict()

        for track in tracks:
            data['tempo'] = track.tempo
            data['energy'] = track.energy
            data['danceability'] = track.danceability
            data['complexity'] = track.complexity
            data['speechiness'] = track.speechiness
            data['loudness'] = track.loudness
            data['valence'] = track.valence
            data['time_signature'] = track.time_signature
            data['key'] = track.key
            data['key_mode'] = track.key_mode
            data['views'] = track.views
            data['likes'] = track.likes
            data['popularity'] = track.likes/track.views

        return data


if __name__ == '__main__':
    cassandra = Cassandra()
    cassandra.create_db_table()


