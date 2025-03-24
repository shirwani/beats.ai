import os
from pathlib import Path
from utils import *
import concurrent.futures
from cassandra.cluster import Cluster
import yt_dlp

cluster = Cluster(['127.0.0.1'], port=9042, connect_timeout=10)
session = cluster.connect('beats_ai')


def record_downloads_info_in_db(downloads, artist):
    print(f"Recording downloads in database for {artist}")

    for d in downloads:
        query = """
            INSERT INTO TRACKS (id, artist, title, genre, url, filename, views, likes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            session.execute(query, (hashify(d['url']), d['artist'], d['title'], d['genre'], d['url'], d['filename'], d['views'], d['likes']))

        except Exception:
            print("Query failed")


def download_tracks_for_artist(artist, genre, max_results=10):
    print(f"Downloading tracks for {artist}")
    download_archive = os.path.join(os.getcwd(), 'dataset', 'download_archive.txt')

    downloads = list()
    ydl_opts = {
        "cookiesfrombrowser": ("chrome",),
        "quiet":            True,
        "noplaylist":       True,
        'extractaudio':     True,
        "default_search":   "ytsearch",
        'format':           'bestaudio/best',
        'audioformat':      'mp3',
        'outtmpl':          os.path.join(os.getcwd(), 'dataset', 'downloads', "%(title)s" + '.%(ext)s'),
        'download_archive': download_archive
    }
    try:
        query = f"{artist} Official"

        # Download tracks
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt_search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=True)

        for entry in yt_search_results.get("entries", []):
            if not entry['like_count']: # sometimes likes are hidden
                print("No likes for download... continuing")
                continue

            # If file has been downloaded successfully, update the database entry
            filename = entry["title"] + '.' + entry["ext"]
            file = os.path.join(os.getcwd(), 'dataset', 'downloads', filename)
            if Path(file).exists():
                downloads.append({
                    "title":    entry["title"],
                    "url":      entry["webpage_url"],
                    "views":    entry["view_count"],
                    "likes":    entry["like_count"],
                    "artist":   artist,
                    "genre":    genre,
                    "filename": filename
                })
            else:
                print(f"Failed to download {entry['webpage_url']}")
    except Exception:
        print(f"Encountered an exception downloading tracks for {artist}")

    record_downloads_info_in_db(downloads, artist)


def discover_and_download_tracks(file, genre, max_workers=10, max_results=10):
    artists = read_list_from_text_file(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for artist in artists:
            executor.submit(download_tracks_for_artist, artist, genre, max_results)


if __name__ == '__main__':
    discover_and_download_tracks('dataset/country_artists.txt', 'country', max_workers=20, max_results=20)
    cluster.shutdown()