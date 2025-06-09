import utils
from Spotify import *
from Youtube import *
from FeatureExtraction import *

cfg = read_from_json_file('config.json')
genre  = cfg['downloads']['genre']

cassandra = Cassandra()

def get_next_artist_to_process():
    artists_to_process = utils.read_list_from_text_file(f"dataset/{genre}.txt")
    artists_processed  = cassandra.get_track_count_for_all_artists()

    for artist in artists_to_process:
        if artist in artists_processed and artists_processed[artist] > 100:
            continue

        print(f"Processing {artist}\n")
        return artist


if __name__ == '__main__':

    artist_name = get_next_artist_to_process()
    print(artist_name)

    if True:
        #cassandra.create_db_table()
        existing_tracks = cassandra.get_track_ids_for_artist(artist_name=artist_name)

    if True:
        #####################################
        # Search Spotify for tracks by artist
        #####################################
        spotify = Spotify()
        tracks = spotify.search_tracks_by_artist(artist_name=artist_name)

    if True:
        ##############################
        # Download tracks from Youtube
        ##############################
        youtube = Youtube()
        downloads = list()
        for track in tracks:
            track_id = hashify(f"{track['artist']} - {track['title']}")
            if track_id in existing_tracks:
                continue
            try:
                downloaded = youtube.download_single_track(artist=track['artist'], title=track['title'], channel=track['artist'])
                downloads.append(downloaded)
            except Exception as e:
                print(e)

        #dump_to_json_file(downloads, f"dataset/{genre}.json")
        #downloads = read_from_json_file(f"dataset/{genre}.json")

    if True:
        ##############################################
        # Shove downloaded tracks' info into Cassandra
        ##############################################
        for downloaded in downloads:
            downloaded['genre'] = genre
            cassandra.record_single_track_info(downloaded)

    if True:
        #############################################################
        # Extract & record features from newly-downloaded audio files
        #############################################################
        tracks = cassandra.get_unanalyzed_tracks()
        f = FeatureExtraction()
        f.extract_features(tracks)

    cassandra.shutdown()
