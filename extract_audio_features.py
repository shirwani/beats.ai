from audio_utils import *
import concurrent.futures
from cassandra.cluster import Cluster
import os
from utils import *
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, TimeoutError

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('beats_ai')

@fcn_logger
def extract_and_update_db(track):
    print(f"Analyzing {track['filename']}")

    file = os.path.join(os.getcwd(), 'dataset', 'downloads', track['filename'])
    f = analyze_audio_features(file)

    if True:
        query = """
        UPDATE TRACKS SET
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

        session.execute(query, (
            f['tempo'],
            f['energy'],
            f['danceability'],
            f['complexity'],
            f['speechiness'],
            f['loudness'],
            f['valence'],
            f['time_signature'],
            f['key'],
            f['key_mode'],
            track['id']))

    print(f"✅ Song record updated for {track['id']}")


def extract_features():
    query = "SELECT * FROM TRACKS"
    tracks = session.execute(query)

    ptracks = list()
    for track in tracks:
        # only do this if we haven't extracted features yet
        if track.key_mode is None:
            ptracks.append(track._asdict())

    with ProcessPoolExecutor(max_workers=5) as executor:
        future_to_track = {executor.submit(extract_and_update_db, track): track for track in ptracks}

        for future in concurrent.futures.as_completed(future_to_track):
            track = future_to_track[future]
            try:
                future.result(timeout=1000)
                print(f"✅ Finished processing: {track['title']}")
            except TimeoutError:
                print(f"⏱️ Timeout: {track['title']}")
            except Exception as e:
                print(f"❌ Error processing {track['title']}: {e}")


if __name__ == '__main__':
    extract_features()
    cluster.shutdown()