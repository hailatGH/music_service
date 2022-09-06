from .models import *

def artist_query(is_album, is_filter, id):
    artist_obj = ArtistModel.objects.filter(id=id).order_by('-created_at').values('id', 'artist_name', 'artist_title', 'artist_cover', 'artist_description', 'user_id', 'created_by', 'created_at', 'updated_at')

def artist_all():
    artist_obj = ArtistModel.objects.all().order_by('-created_at').values('id', 'artist_name', 'artist_title', 'artist_cover', 'artist_description', 'user_id', 'created_by', 'created_at', 'updated_at')
    return artist_obj

def album_filter(is_album, id):
    if is_album:
        album_obj = AlbumModel.objects.filter(id=id).order_by('-created_at').values('id', 'album_title', 'album_cover', 'album_description', 'artist_id', 'album_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    else:
        album_obj = AlbumModel.objects.filter(artist_id=id).order_by('-created_at').values('id', 'album_title', 'album_cover', 'album_description', 'artist_id', 'album_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    return album_obj

def album_all():
    album_obj = AlbumModel.objects.all().order_by('-created_at').values('id', 'album_title', 'album_cover', 'album_description', 'artist_id', 'album_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    return album_obj

def genre_filter(id):
    genre_obj = GenreModel.objects.filter(id=id).values('id', 'genre_title', 'genre_cover', 'genre_description', 'created_by', 'created_at', 'updated_at')
    return genre_obj

def genre_all():
    genre_obj = GenreModel.objects.all().values('id', 'genre_title', 'genre_cover', 'genre_description', 'created_by', 'created_at', 'updated_at')
    return genre_obj

def track_filter(is_track, id):
    if is_track:
        track_obj = TrackModel.objects.filter(id=id).values('id', 'track_name', 'track_description', 'track_file', 'track_cover', 'track_status', 'track_release_date', 'artist_id', 'album_id', 'genre_id', 'track_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    else:
        track_obj = TrackModel.objects.filter(album_id=id).values('id', 'track_name', 'track_description', 'track_file', 'track_cover', 'track_status', 'track_release_date', 'artist_id', 'album_id', 'genre_id', 'track_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    return track_obj

def track_all():
    track_obj = TrackModel.objects.all().values('id', 'track_name', 'track_description', 'track_file', 'track_cover', 'track_status', 'track_release_date', 'artist_id', 'album_id', 'genre_id', 'track_price', 'user_id', 'created_by', 'created_at', 'updated_at')
    return track_obj

def lyrics_filter(id):
    lyrics_obj = LyricsModel.objects.filter(track_id=id).values('id', 'lyrics_title', 'lyrics_detail', 'track_id', 'created_at', 'updated_at')
    return lyrics_obj

def lyrics_all():
    lyrics_obj = LyricsModel.objects.all().values('id', 'lyrics_title', 'lyrics_detail', 'track_id', 'created_at', 'updated_at')
    return lyrics_obj