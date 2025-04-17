from Cassandra import *
from audio_utils import *
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, TimeoutError

cfg = read_from_json_file('config.json')
download_folder     = cfg['downloads']['download_folder']
max_workers         = cfg['downloads']['max_workers']
db_tablename        = cfg['downloads']['db_tablename']

db = Cassandra()

class FeatureExtraction:
    def __init__(self):
        pass

    @fcn_logger
    def extract_and_update_db(self, track):
        print(f"Analyzing {track['filename']}")

        file = os.path.join(os.getcwd(), download_folder, track['filename'])
        features = analyze_audio_features(file)
        db.update_db_track_info(track, features)

        print(f"✅ Song record updated for {track['id']}")

    @fcn_logger
    def extract_features(self, tracks):
        with ProcessPoolExecutor(max_workers) as executor:
            future_to_track = {executor.submit(self.extract_and_update_db, track): track for track in tracks}

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
    f = FeatureExtraction()
    f.extract_features(db.get_unanalyzed_tracks())
    db.shutdown()
