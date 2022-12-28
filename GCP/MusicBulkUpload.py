import os
from pathlib import Path
import json
import requests

# URL = "http://127.0.0.1:8000/webApp/"
# URL = "https://music-service-dev-vdzflryflq-ew.a.run.app/webApp/"
URL = "https://music-service.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/webApp/"
ENCODER_ID = "0Yi6yM0YmDWd55AfF0cYea2iXsc2"

artists_path = sorted(os.listdir('./ROOT/'))
artists = []
for artist_path in artists_path:
    artist = {}
    albums = []

    if os.path.isdir(f'./ROOT/{artist_path}'):
        for artist_file in os.listdir(f'./ROOT/{artist_path}/'):
            artist_file = artist_file.lower()
            if artist_file.endswith(".txt"):
                for line in open(f'./ROOT/{artist_path}/{artist_file}', 'r').readlines():
                    artist[line.strip()[:line.strip().index(':')]] = line.strip()[
                        line.strip().index(':') + 2:]
            if artist_file.endswith(".jpg"):
                artist['artist_profileImage'] = str(
                    os.path.abspath(f'./ROOT/{artist_path}/{artist_file}'))
            if artist_file.endswith(".png"):
                artist['artist_profileImage'] = str(
                    os.path.abspath(f'./ROOT/{artist_path}/{artist_file}'))
            if artist_file.endswith('.jpeg'):
                artist['artist_profileImage'] = str(
                    os.path.abspath(f'./ROOT/{artist_path}/{artist_file}'))

        albums_path = sorted(os.listdir(f'./ROOT/{artist_path}/'))
        for album_path in albums_path:
            album = {}
            tracks = []
            singles = {}
            stracks = []

            if album_path == 'Singles':
                tracks_path = sorted(os.listdir(
                    f'./ROOT/{artist_path}/Singles/'))
                for track_path in tracks_path:
                    track = {}
                    if os.path.isdir(f'./ROOT/{artist_path}/Singles/{track_path}'):
                        for strack_file in os.listdir(f'./ROOT/{artist_path}/Singles/{track_path}'):
                            strack_file = strack_file.lower()
                            if strack_file.endswith(".txt"):
                                if strack_file == "lyrics.txt":
                                    with open(f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}') as lyrics:
                                        lines = lyrics.readlines()
                                        lyrics = ""
                                        for line in lines:
                                            lyrics = lyrics + line
                                        track['track_lyrics'] = lyrics
                                else:
                                    for line in open(f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}', 'r').readlines():
                                        track[line.strip()[:line.strip().index(':')]] = line.strip()[
                                            line.strip().index(':') + 2:]

                            if strack_file.endswith(".jpg"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))
                            if strack_file.endswith(".png"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))
                            if strack_file.endswith(".jpeg"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))

                            if strack_file.endswith(".aac"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))
                            if strack_file.endswith(".mp3"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))
                            if strack_file.endswith(".wav"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/Singles/{track_path}/{strack_file}'))

                        stracks.append(track)
                artist['Singles'] = stracks
                continue

            if os.path.isdir(f'./ROOT/{artist_path}/{album_path}'):
                for album_file in os.listdir(f'./ROOT/{artist_path}/{album_path}'):
                    album_file = album_file.lower()
                    if album_file.endswith(".txt"):
                        for line in open(f'./ROOT/{artist_path}/{album_path}/{album_file}', 'r').readlines():
                            album[line.strip()[:line.strip().index(':')]] = line.strip()[
                                line.strip().index(':') + 2:]
                    if album_file.endswith(".jpg"):
                        album['album_coverImage'] = str(os.path.abspath(
                            f'./ROOT/{artist_path}/{album_path}/{album_file}'))
                    if album_file.endswith(".png"):
                        album['album_coverImage'] = str(os.path.abspath(
                            f'./ROOT/{artist_path}/{album_path}/{album_file}'))
                    if album_file.endswith(".jpeg"):
                        album['album_coverImage'] = str(os.path.abspath(
                            f'./ROOT/{artist_path}/{album_path}/{album_file}'))

                tracks_path = sorted(os.listdir(
                    f'./ROOT/{artist_path}/{album_path}/'))
                for track_path in tracks_path:
                    track = {}
                    if os.path.isdir(f'./ROOT/{artist_path}/{album_path}/{track_path}'):
                        for track_file in os.listdir(f'./ROOT/{artist_path}/{album_path}/{track_path}'):
                            track_file = track_file.lower()
                            if track_file.endswith(".txt"):
                                if track_file == "lyrics.txt":
                                    with open(f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}') as lyrics:
                                        lines = lyrics.readlines()
                                        lyrics = ""
                                        for line in lines:
                                            lyrics = lyrics + line
                                        track['track_lyrics'] = lyrics
                                else:
                                    for line in open(f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}', 'r').readlines():
                                        track[line.strip()[:line.strip().index(':')]] = line.strip()[
                                            line.strip().index(':') + 2:]

                            if track_file.endswith(".jpg"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))
                            if track_file.endswith(".png"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))
                            if track_file.endswith(".jpeg"):
                                track['track_coverImage'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))

                            if track_file.endswith(".aac"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))
                            if track_file.endswith(".mp3"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))
                            if track_file.endswith(".wav"):
                                track['track_audioFile'] = str(os.path.abspath(
                                    f'./ROOT/{artist_path}/{album_path}/{track_path}/{track_file}'))

                        tracks.append(track)

                album['Tracks'] = tracks
                albums.append(album)

        artist['Albums'] = albums
        artists.append(artist)

# print(artists)

for i in range(len(artists)):
    artist = artists[i]

    artistFiles = {
        'artist_profileImage': open(artist['artist_profileImage'], 'rb')
    }
    artist_response = requests.post(URL + "artist", data=({
        "artist_name": artist['artist_name'],
        "artist_title": artist['artist_title'],
        "artist_rating": 0,
        "artist_status": "true",
        "artist_releaseDate": artist['artist_releaseDate'],
        "artist_description": artist['artist_description'],
        "artist_viewcount": 0,
        "artist_FUI": artist['artist_FUI'],
        "encoder_FUI": ENCODER_ID,
    }), files=artistFiles)

    print(f"Artist: ", artist['artist_name'],
          "Status : ", artist_response.status_code)

    if artist_response.status_code == 201:
        artist['id'] = json.loads(artist_response.content)['id']

        if len(artist['Singles']):
            album_id = requests.get(
                f"{URL}albumIdByAlbumName?album_name={artist['artist_name']}_Singles")

            for s in range(len(artist['Singles'])):
                track = artist['Singles'][s]

                trackFiles = {
                    'track_coverImage': open(track['track_coverImage'], 'rb'),
                    'track_audioFile': open(track['track_audioFile'], 'rb'),
                }
                track_response = requests.post(URL + "track", data=({
                    "track_name": track['track_name'],
                    "track_rating": 0,
                    "track_status": "true",
                    "track_releaseDate": track['track_releaseDate'],
                    "track_description": track['track_description'],
                    "track_viewcount": 0,
                    "track_lyrics": track['track_lyrics'],
                    "track_price": track['track_price'],
                    "artists_featuring": track['artists_featuring'],
                    "encoder_FUI": ENCODER_ID,
                    "artist_id": artist['id'],
                    "album_id": album_id,
                    "genre_id": track['genre_id'],
                }), files=trackFiles)

                print(f"Track: ", track['track_name'],
                      "Status : ", track_response.status_code)

        for j in range(len(artist['Albums'])):
            album = artist['Albums'][j]

            albumFiles = {
                'album_coverImage': open(album['album_coverImage'], 'rb')
            }
            album_response = requests.post(URL + "album", data=({
                "album_name": album['album_name'],
                "album_rating": 0,
                "album_status": "true",
                "album_releaseDate": album['album_releaseDate'],
                "album_description": album['album_description'],
                "album_viewcount": 0,
                "album_price": int(album['album_price']),
                "artist_id": artist['id'],
                "encoder_FUI": ENCODER_ID,
            }), files=albumFiles)

            print(f"Album: ", album['album_name'],
                  "Status : ", album_response.status_code)
            if album_response.status_code == 201:
                album['id'] = json.loads(album_response.content)['id']

                for k in range(len(album['Tracks'])):
                    track = album['Tracks'][k]

                    trackFiles = {
                        'track_coverImage': open(track['track_coverImage'], 'rb'),
                        'track_audioFile': open(track['track_audioFile'], 'rb'),
                    }
                    track_response = requests.post(URL + "track", data=({
                        "track_name": track['track_name'],
                        "track_rating": 0,
                        "track_status": "true",
                        "track_releaseDate": track['track_releaseDate'],
                        "track_description": track['track_description'],
                        "track_viewcount": 0,
                        "track_lyrics": track['track_lyrics'],
                        "track_price": track['track_price'],
                        "artists_featuring": track['artists_featuring'],
                        "encoder_FUI": ENCODER_ID,
                        "artist_id": artist['id'],
                        "album_id": album['id'],
                        "genre_id": track['genre_id'],
                    }), files=trackFiles)

                    print(f"Track: ", track['track_name'],
                          "Status : ", track_response.status_code)
