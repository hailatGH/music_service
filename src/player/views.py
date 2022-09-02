from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import ArtistModel, AlbumModel, GenreModel, TrackModel, LyricsModel, PlayListModel, PlayListTracksModel, FavouritesModel
from .serializers import ArtistSerializer, AlbumSerializer, GenreSerializer, TrackSerializer, LyricsSerializer, FavouritesSerializer, PlayListSerializer, PlayListTracksSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
class ArtistViewSet(viewsets.ModelViewSet):
    
    queryset = ArtistModel.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        artists = []
        try:
            artist_obj = ArtistModel.objects.all().order_by('-created_at').values("id", "artist_name", "artist_cover")
        
            for k in range(len(artist_obj)):
                artist = {}
                albums = []
                single_tracks = []
                
                artist_id = artist_obj[k]['id']
                artist_name = artist_obj[k]['artist_name']
                artist_cover = artist_obj[k]['artist_cover']

                for variable in ["artist_id", "artist_name", "artist_cover"]:
                    artist[variable] = eval(variable)

                album_obj = AlbumModel.objects.filter(artist_id=artist_id).order_by('-created_at').values("id", "album_title", "album_cover")
                for i in range(len(album_obj)):
                    album = {}
                    tracks = []

                    album = {}
                    album_id = album_obj[i]['id']
                    album_title = album_obj[i]['album_title']
                    album_cover = album_obj[i]['album_cover']

                    for variable in ["album_id", "album_title", "album_cover"]:
                        album[variable] = eval(variable)

                    track_obj = TrackModel.objects.filter(album_id=album_id).values('id', 'track_name', 'track_file', 'genre_id')
                    for j in range(len(track_obj)):
                        track_data = {}

                        track_id = track_obj[j]['id']
                        track_name = track_obj[j]['track_name']
                        track_file = track_obj[j]['track_file']
                        genre_id = track_obj[j]['genre_id']
                        genre_name = GenreModel.objects.filter(id=genre_id).values('genre_title')[0]['genre_title']
                        try:
                            lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                            lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                        except:
                            lyrics_id = ""
                            lyrics_detail = ""

                        for variable in ["track_id", "track_name", "track_file", "genre_id", "genre_name", "lyrics_id", "lyrics_detail"]:
                            track_data[variable] = eval(variable)
                        tracks.append(track_data)
                    album["Tracks"] = tracks
                    albums.append(album)
                artist["single_tracks"] = single_tracks
                artist["albums"] = albums
                artists.append(artist)
        except:
            artists = []
        return Response(artists)

class AlbumViewSet(viewsets.ModelViewSet):
    
    queryset = AlbumModel.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        albums = []
        try:
            album_obj = AlbumModel.objects.all().order_by('-created_at').values('id', 'album_title', 'album_cover', 'artist_id')

            for j in range(len(album_obj)):
                album = {}
                tracks = []

                album_data = {}
                album_id = album_obj[j]['id']
                album_title = album_obj[j]['album_title']
                album_cover = album_obj[j]['album_cover']
                artist_id = album_obj[j]['artist_id']
                artist_name = ArtistModel.objects.filter(id=artist_id).values('artist_name')[0]['artist_name']

                for variable in ["album_id", "album_title", "album_cover", "artist_id", "artist_name"]:
                    album[variable] = eval(variable)

                track_obj = TrackModel.objects.filter(album_id=album_id).values('id', 'track_name', 'track_file', 'genre_id')
                
                for i in range(len(track_obj)):
                    track_data = {}

                    track_id = track_obj[i]['id']
                    track_name = track_obj[i]['track_name']
                    track_file = track_obj[i]['track_file']
                    genre_id = track_obj[i]['genre_id']
                    genre_name = GenreModel.objects.filter(id=genre_id).values('genre_title')[0]['genre_title']
                    try:
                        lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                        lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                    except:
                        lyrics_id = ""
                        lyrics_detail = ""

                    for variable in ["track_id", "track_name", "track_file", "genre_id", "genre_name", "lyrics_id", "lyrics_detail"]:
                        track_data[variable] = eval(variable)

                    tracks.append(track_data)
                album["Tracks"] = tracks
                albums.append(album)
        except:
            albums = []
        return Response(albums)
class GenreViewSet(viewsets.ModelViewSet):
    
    queryset = GenreModel.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        genres = []
        try:
            genre_obj = GenreModel.objects.all().order_by('-created_at').values('id', 'genre_title', 'genre_cover')

            for j in range(len(genre_obj)):
                genre = {}
                tracks = []

                genre_id = genre_obj[j]['id']
                genre_title = genre_obj[j]['genre_title']
                genre_cover = genre_obj[j]['genre_cover']

                for variable in ["genre_id", "genre_title", "genre_cover"]:
                    genre[variable] = eval(variable)
                
                track_obj = TrackModel.objects.filter(genre_id=genre_id).order_by('-created_at').values('id', 'track_name', 'track_file', 'artist_id', 'album_id')
                for i in range(len(track_obj)):
                    track_data = {}

                    track_id = track_obj[i]['id']
                    track_name = track_obj[i]['track_name']
                    track_file = track_obj[i]['track_file']
                    artist_id = track_obj[i]['artist_id']
                    artist_name = ArtistModel.objects.filter(id=track_obj[i]['artist_id']).values('artist_name')[0]['artist_name']
                    album_id = track_obj[i]['album_id']
                    album_title = AlbumModel.objects.filter(id=track_obj[i]['album_id']).values('album_title')[0]['album_title']
                    album_cover = AlbumModel.objects.filter(id=track_obj[i]['album_id']).values('album_cover')[0]['album_cover']
                    try:
                        lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                        lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                    except:
                        lyrics_id = ""
                        lyrics_detail = ""
                    
                    for variable in ["track_id", "track_name", "track_file", "artist_id", "artist_name", "album_id", "album_title", "album_cover", "lyrics_id", "lyrics_detail"]:
                        track_data[variable] = eval(variable)

                    tracks.append(track_data)
                genre["Tracks"] = tracks
                genres.append(genre)  
        except:
            genres = []
        return Response(genres)
class TrackViewSet(viewsets.ModelViewSet):
    
    queryset = TrackModel.objects.all()
    serializer_class = TrackSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        tracks = []
        try:
            track_obj = TrackModel.objects.all().order_by('-created_at').values('id', 'track_name', 'track_file', 'artist_id', 'album_id', "genre_id")
            for i in range(len(track_obj)):
                track_data = {}

                track_id = track_obj[i]['id']
                track_name = track_obj[i]['track_name']
                track_file = track_obj[i]['track_file']
                artist_id = track_obj[i]['artist_id']
                artist_name = ArtistModel.objects.filter(id=track_obj[i]['artist_id']).values('artist_name')[0]['artist_name']
                album_id = track_obj[i]['album_id']
                album_title = AlbumModel.objects.filter(id=track_obj[i]['album_id']).values('album_title')[0]['album_title']
                album_cover = AlbumModel.objects.filter(id=track_obj[i]['album_id']).values('album_cover')[0]['album_cover']
                genre_id = track_obj[i]['genre_id']
                genre_title = GenreModel.objects.filter(id=track_obj[i]['genre_id']).values('genre_title')[0]['genre_title']
                try:
                    lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                    lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                except:
                    lyrics_id = ""
                    lyrics_detail = ""
                
                for variable in ["track_id", "track_name", "track_file", "artist_id", "artist_name", "album_id", "album_title", "album_cover", "genre_id", "genre_title", "lyrics_id", "lyrics_detail"]:
                    track_data[variable] = eval(variable)
                tracks.append(track_data)
        except:
            tracks = []
        return Response(tracks)
class LyricsViewSet(viewsets.ModelViewSet):
    
    queryset = LyricsModel.objects.all().order_by('-created_at')
    serializer_class = LyricsSerializer
    pagination_class = StandardResultsSetPagination
class PlayListViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListModel.objects.all()
    serializer_class = PlayListSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        playlists = []
        try:
            playlist_obj = PlayListModel.objects.filter(user_id=request.query_params['user']).values('id', 'playlist_name', 'user_id')

            for j in range(len(playlist_obj)):
                playlist = {}
                tracks = []

                playlist_id = playlist_obj[j]['id']
                playlist_name = playlist_obj[j]['playlist_name']
                user_id = playlist_obj[j]['user_id']

                for variable in ["playlist_id", "playlist_name", "user_id"]:
                    playlist[variable] = eval(variable)

                playlist_tracks_obj = PlayListTracksModel.objects.filter(playlist_id=playlist_id).values('id', 'playlist_id', 'track_id')   

                for i in range(len(playlist_tracks_obj)):
                    track_data = {}

                    track_obj = TrackModel.objects.filter(id=playlist_tracks_obj[i]['track_id']).values('id', 'track_name', 'track_file', 'artist_id', 'album_id', "genre_id")
                    
                    playlisttracks_id = playlist_tracks_obj[i]['id']
                    track_id = track_obj[0]['id']
                    track_name = track_obj[0]['track_name']
                    track_file = track_obj[0]['track_file']
                    artist_id = track_obj[0]['artist_id']
                    artist_name = ArtistModel.objects.filter(id=track_obj[0]['artist_id']).values('artist_name')[0]['artist_name']
                    album_id = track_obj[0]['album_id']
                    album_title = AlbumModel.objects.filter(id=track_obj[0]['album_id']).values('album_title')[0]['album_title']
                    album_cover = AlbumModel.objects.filter(id=track_obj[0]['album_id']).values('album_cover')[0]['album_cover']
                    genre_id = track_obj[0]['genre_id']
                    genre_title = GenreModel.objects.filter(id=track_obj[0]['genre_id']).values('genre_title')[0]['genre_title']
                    try:
                        lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                        lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                    except:
                        lyrics_id = ""
                        lyrics_detail = ""

                    for variable in ["playlisttracks_id", "track_id", "track_name", "track_file", "artist_id", "artist_name", "album_id", "album_title", "album_cover", "genre_id", "genre_title", "lyrics_id", "lyrics_detail"]:
                        track_data[variable] = eval(variable)
                    
                    tracks.append(track_data)
                playlist["Tracks"] = tracks
                playlists.append(playlist)      
        except:
            playlists = []
        return Response(playlists)

class PlayListTracksViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListTracksModel.objects.all()
    serializer_class = PlayListTracksSerializer
    pagination_class = StandardResultsSetPagination
class FavouritesViewSet(viewsets.ModelViewSet):

    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        favourite_data = {}
        tracks = []

        try:
            favourite_obj = FavouritesModel.objects.filter(user_id=request.query_params['user']).values('id', 'user_id', 'track_id')
            user_id = favourite_obj[0]['user_id']
            favourite_data["User"] = user_id

            for i in range(len(favourite_obj)):
                track_data = {}
            
                track_obj = TrackModel.objects.filter(id=favourite_obj[i]['track_id']).values('id', 'track_name', 'track_file', 'artist_id', 'album_id', "genre_id")
                favourites_id = favourite_obj[i]['id']
                track_id = track_obj[0]['id']
                track_name = track_obj[0]['track_name']
                track_file = track_obj[0]['track_file']
                artist_id = track_obj[0]['artist_id']
                artist_name = ArtistModel.objects.filter(id=track_obj[0]['artist_id']).values('artist_name')[0]['artist_name']
                album_id = track_obj[0]['album_id']
                album_title = AlbumModel.objects.filter(id=track_obj[0]['album_id']).values('album_title')[0]['album_title']
                album_cover = AlbumModel.objects.filter(id=track_obj[0]['album_id']).values('album_cover')[0]['album_cover']
                genre_id = track_obj[0]['genre_id']
                genre_title = GenreModel.objects.filter(id=track_obj[0]['genre_id']).values('genre_title')[0]['genre_title']
                try:
                    lyrics_id = LyricsModel.objects.filter(track_id=track_id).values('id')[0]['id']
                    lyrics_detail = LyricsModel.objects.filter(track_id=track_id).values('lyrics_detail')[0]['lyrics_detail']
                except:
                    lyrics_id = ""
                    lyrics_detail = ""

                for variable in ["favourites_id", "track_id", "track_name", "track_file", "artist_id", "artist_name", "album_id", "album_title", "album_cover", "genre_id", "genre_title", "lyrics_id", "lyrics_detail"]:
                    track_data[variable] = eval(variable)
                
                tracks.append(track_data)
            favourite_data["Tracks"] = tracks
        except:
            favourite_data = {}
        return Response(favourite_data)