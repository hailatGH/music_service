from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'

class DataByUserId(viewsets.ModelViewSet):
    
    queryset = ArtistModel.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        data = []
        try:
            id = request.query_params['id']
            level = int(request.query_params['level'])

            if (level == 0):
                data.append("Comapny")
            elif (level == 1):
                artist_obj = ArtistModel.objects.filter(created_by=id).values('id', 'artist_name', 'artist_cover')
                page = self.paginate_queryset(artist_obj)
                for artist_count in range(len(page)):
                    artist = {}
                    albums = []

                    for val in ['id', 'artist_name', 'artist_cover']:
                        id = 'id'
                        artist[val] = page[artist_count][val]
                    
                    all_album_obj = AlbumModel.objects.filter(artist_id=page[artist_count]['id']).values('id', 'album_title', 'album_cover')
                    album_obj = all_album_obj.exclude(album_title='Singles')
                    for album_count in range(len(album_obj)):
                        album = {}
                        tracks = []

                        for val in ['id', 'album_title', 'album_cover']:
                            album[val] = album_obj[album_count][val]

                        track_obj = TrackModel.objects.filter(album_id=album_obj[album_count]['id']).values('id', 'track_name', 'track_cover')
                        for track_count in range(len(track_obj)):
                            track = {}

                            for val in ['id', 'track_name', 'track_cover']:
                                track[val] = track_obj[track_count][val]

                            tracks.append(track)

                        album["Tracks"] = tracks
                        albums.append(album)

                    artist["Albums"] = albums

                    singles_id = all_album_obj.filter(album_title='Singles')[0]['id']
                    try:
                        single_track_obj = TrackModel.objects.filter(album_id=singles_id).values('id', 'track_name', 'track_cover')
                    except:
                        single_track_obj = []
                    single_tracks = []
                    for track_count in range(len(single_track_obj)):
                        track = {}
                        for val in ['id', 'track_name', 'track_cover']:
                            track[val] = single_track_obj[track_count][val]
                        single_tracks.append(track)
                    artist['Singles'] = single_tracks
                    data.append(artist)
            elif (level == 2):
                all_album_obj = AlbumModel.objects.filter(user_id=id).values('id', 'album_title', 'album_cover')
                album_obj = all_album_obj.exclude(album_title='Singles')
                for album_count in range(len(album_obj)):
                    album = {}
                    tracks = []

                    for val in ['id', 'album_title', 'album_cover']:
                        album[val] = album_obj[album_count][val]

                    track_obj = TrackModel.objects.filter(album_id=album_obj[album_count]['id']).values('id', 'track_name', 'track_cover')
                    for track_count in range(len(track_obj)):
                        track = {}

                        for val in ['id', 'track_name', 'track_cover']:
                            track[val] = track_obj[track_count][val]

                        tracks.append(track)

                    album["Tracks"] = tracks
                    data.append(album)
                
                singles = {}
                single_tracks = []
                singles_obj = all_album_obj.filter(album_title='Singles')
                for val in ['id', 'album_title', 'album_cover']:
                    singles[val] = singles_obj[0][val]
                try:
                    single_track_obj = TrackModel.objects.filter(album_id=singles_obj[0]['id']).values('id', 'track_name', 'track_cover')
                except:
                    single_track_obj = []

                for track_count in range(len(single_track_obj)):
                    track = {}
                    for val in ['id', 'track_name', 'track_cover']:
                        track[val] = single_track_obj[track_count][val]
                    single_tracks.append(track)
                singles['Singles'] = single_tracks
                data.append(singles)
        except:
            data = []
        return Response(data)

class PopularMusicViewSet(viewsets.ModelViewSet):

    queryset = TrackModel.objects.all()
    serializer_class = TrackSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        data = []
        track_obj = self.queryset.order_by('-viewcount').values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
        page = self.paginate_queryset(track_obj)
        if page is not None:  
            # serializer = self.get_serializer(page, many=True)
            for track_count in range(len(page)):
                track = {}
                artist = {}
                album = {}
                genre = {}
                lyrics = {}
                for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                    track[val] = page[track_count][val]
                
                artist_obj = ArtistModel.objects.filter(id=page[track_count]['artist_id']).values('id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at')
                for val in ['id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at']:
                    artist[val] = artist_obj[0][val]
                track['artist_name'] = artist_obj[0]['artist_name']
                track['Artist'] = artist

                album_obj = AlbumModel.objects.filter(id=page[track_count]['album_id']).values('id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at')
                for val in ['id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at']:
                    album[val] = album_obj[0][val]
                track['Album'] = album

                genre_obj = GenreModel.objects.filter(id=page[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                    genre[val] = genre_obj[0][val]
                track['Genre'] = genre

                try:
                    lyrics_obj = LyricsModel.objects.filter(id=page[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                    for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                        lyrics[val] = lyrics_obj[0][val]
                    track['Lyrics'] = lyrics
                except:
                    track['Lyrics'] = ""
                data.append(track)
        return Response(data)

class TracksViewSet(viewsets.ModelViewSet):

    queryset = TrackModel.objects.all().exclude(track_status=True)
    serializer_class = TrackSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        tracks = []
        track_obj = self.queryset.order_by('-created_at').values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
        page = self.paginate_queryset(track_obj)
        if page is not None:  
            # serializer = self.get_serializer(page, many=True)
            for track_count in range(len(page)):
                track = {}
                artist = {}
                album = {}
                genre = {}
                lyrics = {}

                for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                    track[val] = page[track_count][val]
                
                artist_obj = ArtistModel.objects.filter(id=page[track_count]['artist_id']).values('id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at')
                track['artist_name'] = artist_obj[0]['artist_name']
                for val in ['id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at']:
                    artist[val] = artist_obj[0][val]
                    track['Artist'] = artist
                
                album_obj = AlbumModel.objects.filter(id=page[track_count]['album_id']).values('id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at')
                for val in ['id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at']:
                    album[val] = album_obj[0][val]
                    track['Album'] = album

                genre_obj = GenreModel.objects.filter(id=page[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                    genre[val] = genre_obj[0][val]
                    track['Genre'] = genre
                try:
                    lyrics_obj = LyricsModel.objects.filter(track_id=page[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                    for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                        lyrics[val] = lyrics_obj[0][val]
                        track['Lyrics'] = lyrics
                except:
                    track['Lyrics'] = ""
                tracks.append(track)

        return Response(tracks)

class ALbumsViewSet(viewsets.ModelViewSet):

    queryset = AlbumModel.objects.all().exclude(album_title="Singles")
    serializer_class = AlbumSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        albums = []
        album_obj = self.queryset.order_by('-created_at').values('id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at')
        page = self.paginate_queryset(album_obj)
        if page is not None:
            for album_count in range(len(page)):
                album = {}
                artist = {}
                tracks = []
                for val in ['id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at']:
                    album[val] = album_obj[album_count][val]
                
                artist_obj = ArtistModel.objects.filter(id=page[album_count]['artist_id']).values('id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at')
                album['artist_name'] = artist_obj[0]['artist_name']
                for val in ['id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at']:
                    artist[val] = artist_obj[0][val]
                    album['Artist'] = artist
                
                track_obj = TrackModel.objects.filter(album_id=page[album_count]['id']).values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
                for track_count in range(len(track_obj)):
                    track = {}
                    genre = {}
                    lyrics = {}
                    for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                        track[val] = track_obj[track_count][val]
                    track['artist_name'] = artist_obj[0]['artist_name']
                    genre_obj = GenreModel.objects.filter(id=track_obj[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                    for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                        genre[val] = genre_obj[0][val]
                        track['Genre'] = genre

                    try:
                        lyrics_obj = LyricsModel.objects.filter(track_id=track_obj[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                        for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                            lyrics[val] = lyrics_obj[0][val]
                            track['Lyrics'] = lyrics
                    except:
                        track['Lyrics'] = ""
                    tracks.append(track)
                album['Tracks'] = tracks
                albums.append(album)

        return Response(albums)

class ArtistsViewSet(viewsets.ModelViewSet):

    queryset = ArtistModel.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        artists = []
        artist_obj = self.queryset.order_by('-created_at').values('id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at')
        page = self.paginate_queryset(artist_obj)
        if page is not None:
            for artist_count in range(len(artist_obj)):
                artist = {}
                albums = []
                tracks = []

                for val in ['id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at']:
                    artist[val] = artist_obj[artist_count][val]
                
                album_obj = AlbumModel.objects.filter(artist_id=page[artist_count]['id']).values('id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at')
                for album_count in range(len(album_obj)):
                    album = {}
                    tracks = []
                    for val in ['id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at']:
                        album[val] = album_obj[album_count][val]
                    album['artist_name'] = page[artist_count]['artist_name']
                    albums.append(album)

                    # track_obj = TrackModel.objects.filter(album_id=album_obj[artist_count]['id']).values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
                    # for track_count in range(len(track_obj)):
                    #     track = {}
                    #     genre = {}
                    #     lyrics = {}
                    #     for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                    #         track[val] = track_obj[track_count][val]
                    #     track['artist_name'] = page[artist_count]['artist_name']
                    #     genre_obj = GenreModel.objects.filter(id=track_obj[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                    #     for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                    #         genre[val] = genre_obj[0][val]
                    #         track['Genre'] = genre

                    #     try:
                    #         lyrics_obj = LyricsModel.objects.filter(track_id=track_obj[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                    #         for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                    #             lyrics[val] = lyrics_obj[0][val]
                    #             track['Lyrics'] = lyrics
                    #     except:
                    #         track['Lyrics'] = ""
                    #     tracks.append(track)                        

                artist['Albums'] = albums

                track_obj = TrackModel.objects.filter(artist_id=page[artist_count]['id']).values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
                for track_count in range(len(track_obj)):
                    track = {}
                    genre = {}
                    lyrics = {}
                    for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                        track[val] = track_obj[track_count][val]
                    track['artist_name'] = page[artist_count]['artist_name']
                    genre_obj = GenreModel.objects.filter(id=track_obj[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                    for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                        genre[val] = genre_obj[0][val]
                        track['Genre'] = genre

                    try:
                        lyrics_obj = LyricsModel.objects.filter(track_id=track_obj[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                        for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                            lyrics[val] = lyrics_obj[0][val]
                            track['Lyrics'] = lyrics
                    except:
                        track['Lyrics'] = ""
                    tracks.append(track)
                artist['Tracks'] = tracks
                artists.append(artist)
        return Response(artists)
class GenresViewSet(viewsets.ModelViewSet):

    queryset = GenreModel.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        genres = []
        genre_obj = self.queryset.values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
        page = self.paginate_queryset(genre_obj)
        if page is not None:
            for genre_count in range(len(page)):
                genre = {}
                tracks = []
                for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                    genre[val] = page[genre_count][val]
                
                track_obj = TrackModel.objects.filter(genre_id=page[genre_count]['id']).values('id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at')
                for track_count in range(len(track_obj)):
                    track = {}
                    artist = {}
                    album = {}
                    genre_t = {}
                    lyrics = {}

                    for val in ['id','track_name','track_description','track_file','track_cover','track_status','track_release_date','artist_id','album_id','genre_id','track_price','user_id','created_by','viewcount','created_at','updated_at']:
                        track[val] = track_obj[track_count][val]
                    track['genre_title'] = page[genre_count]['genre_title']

                    artist_obj = ArtistModel.objects.filter(id=track_obj[track_count]['artist_id']).values('id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at')
                    track['artist_name'] = artist_obj[0]['artist_name']
                    for val in ['id','artist_name','artist_title','artist_cover','artist_description','user_id','created_by','created_at','updated_at']:
                        artist[val] = artist_obj[0][val]
                        track['Artist'] = artist
                    
                    album_obj = AlbumModel.objects.filter(id=track_obj[track_count]['album_id']).values('id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at')
                    for val in ['id','album_title','album_cover','album_description','artist_id','album_price','user_id','created_by','created_at','updated_at']:
                        album[val] = album_obj[0][val]
                        track['Album'] = album                    
                    
                    genre_obj_t = GenreModel.objects.filter(id=track_obj[track_count]['genre_id']).values('id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at')
                    for val in ['id','genre_title','genre_cover','genre_description','created_by','created_at','updated_at']:
                        genre_t[val] = genre_obj_t[0][val]
                        track['Genre'] = genre_t
                    try:
                        lyrics_obj = LyricsModel.objects.filter(track_id=track_obj[track_count]['id']).values('id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at')
                        for val in ['id','lyrics_title','lyrics_detail','track_id','created_by','created_at','updated_at']:
                            lyrics[val] = lyrics_obj[0][val]
                            track['Lyrics'] = lyrics
                    except:
                        track['Lyrics'] = ""
                    tracks.append(track)
                genre['Tracks'] = tracks
                genres.append(genre)
        
        return Response(genres)