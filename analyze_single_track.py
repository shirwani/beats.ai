import yt_dlp
from audio_utils import *
from utils import *
import os
from pathlib import Path


def download_track(url, filename, output_folder="samples"):
    ydl_opts = {
        "cookiesfrombrowser": ("chrome",),
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/{filename}',
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    download = {
        "views":    info.get("view_count"),
        "likes":    info.get("like_count")
    }
    return download

target = [
    {'filename': 'coldsea',     'url': 'https://www.youtube.com/watch?v=RbI9PrDk9Lg'},
    {'filename': 'downfall',    'url': 'https://www.youtube.com/watch?v=_fZdiVvdghE'},
    {'filename': 'nightshift',  'url': 'https://www.youtube.com/watch?v=cZgdJ1l4cDM'},
    {'filename': 'amends',      'url': 'https://www.youtube.com/watch?v=VQQLb4xQODA'},
    {'filename': 'blackforest', 'url': 'https://www.youtube.com/watch?v=1LZczseDR3Q'},
    {'filename': 'lasers',      'url': 'https://www.youtube.com/watch?v=nLjr0s-5Ba0'},
    {'filename': 'divinedrip',  'url': 'https://www.youtube.com/watch?v=3SUBxpXtxnA'},
    {'filename': 'isolation',   'url': 'https://www.youtube.com/watch?v=5_2mSNWKQCA'},
    {'filename': 'standbyme',   'url': 'https://www.youtube.com/watch?v=lg8BHXF2iNo'},
    {'filename': 'predator',    'url': 'https://www.youtube.com/watch?v=j3v7vctehHQ'},
    {'filename': 'redemption',  'url': 'https://www.youtube.com/watch?v=32oCDJv6wAA'},
    {'filename': 'intofire',    'url': 'https://www.youtube.com/watch?v=Egep0xMHQ4c'},
    {'filename': 'journey',     'url': 'https://www.youtube.com/watch?v=EhTRPoHpc8c'},
    {'filename': 'dreams',      'url': 'https://www.youtube.com/watch?v=3fbfAC9nyII'},
    {'filename': 'electro',     'url': 'https://www.youtube.com/watch?v=oQiwUh-YbUE'},
    {'filename': 'moonrise',    'url': 'https://www.youtube.com/watch?v=_4TIMZq_7Iw'},
    {'filename': 'freestyle',   'url': 'https://www.youtube.com/watch?v=uC_niLaYvyY'}
]


results = dict()
for t in target:
    download = download_track(t['url'], t['filename'])
    f = analyze_audio_features(f"samples/{t['filename']}.mp3")
    results[t['filename']] = f

    print(download)
    print(results[t['filename']])

    results[t['filename']]['views'] = download['views']
    results[t['filename']]['likes'] = download['likes']


dump_to_json_file(results, "hackaz.json")

