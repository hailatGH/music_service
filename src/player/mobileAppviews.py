from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

# Standard Results Set Pagination 
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    
# Class based model viewsets for the Mobile App

class ArtistsByUserId(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer
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
        userId = request.query_params['userId']
        try:
            artists = self.queryset.filter(artist_status=True, encoder_FUI=userId).order_by('-created_at').values('id','artist_name','artist_profileImage')
            page = self.paginate_queryset(artists)
        except BaseException as e:
            page = str(e)
        return Response(page)

class AlbumsByUserId(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
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
        userId = request.query_params['userId']
        try:
            albums = self.queryset.filter(album_status=True, encoder_FUI=userId).exclude(album_name__contains="_Singles").order_by('-created_at').values('id','album_name','album_coverImage')
            page = self.paginate_queryset(albums)
        except BaseException as e:
            page = str(e)
        return Response(page)

class TracksByUserId(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
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
        userId = request.query_params['userId']
        try:
            tracks = self.queryset.filter(track_status=True, encoder_FUI=userId).order_by('-created_at').values('id','track_name','track_coverImage')
            page = self.paginate_queryset(tracks)
        except BaseException as e:
            page = str(e)
        return Response(page)

class ArtistsMobileViewSet(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer
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
        try:
            artists = self.queryset.filter(artist_status=True).order_by('-created_at').values('id','artist_name','artist_profileImage')
            page = self.paginate_queryset(artists)
            if page is not None:
                for artist_count in range(len(page)):
                    if AlbumsModel.objects.filter(album_status=True, artist_id=page[artist_count]['id']).exists():
                        albums = AlbumsModel.objects.filter(album_status=True, artist_id=page[artist_count]['id'])
                        page[artist_count]['noOfAlbums'] = albums.count() - 1
                        try:
                            page[artist_count]['noOfTracks'] = TracksModel.objects.filter(track_status=True, album_id=albums.filter(album_name='Singles').values('id')[0]['id']).count()
                        # if TracksModel.objects.filter(track_status=True, album_id=albums.filter(album_name='Singles').values('id')[0]['id']).exists():
                        #     page[artist_count]['noOfTracks'] = 1
                            # page[artist_count]['noOfTracks'] = TracksModel.objects.filter(track_status=True, album_id=albums.filter(album_name='Singles').values('id')[0]['id']).count()
                        # else:
                        except:
                            page[artist_count]['noOfTracks'] = 0
                    else:
                        page[artist_count]['noOfAlbums'] = 0
                        page[artist_count]['noOfTracks'] = 0
        except BaseException as e:
            page = str(e)
        return Response(page)

class AlbumByArtistIdViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
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
        userId = request.query_params['userId']
        artistId = request.query_params['artistId']
        albums = self.queryset.filter(album_status=True, artist_id=artistId).order_by('-created_at').values('id','album_name','album_coverImage','album_description','album_price','artist_id')
        page = self.paginate_queryset(albums)
        if page is not None:
            for album_count in range(len(page)):
                artists = ArtistsModel.objects.filter(id=page[album_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):    
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[album_count]['artist_name'] = artist_name
                page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(album_id=page[album_count]['id'], user_FUI=userId).exists()
                if TracksModel.objects.filter(track_status=True, album_id=page[album_count]['id']).exists():
                    page[album_count]['noOfTracks'] = TracksModel.objects.filter(track_status=True, album_id=page[album_count]['id']).count()
                else:
                     page[album_count]['noOfTracks'] = 0
        return Response(page)

class AlbumsMobileViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
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
        userId = request.query_params['userId']
        albums = self.queryset.filter(album_status=True).order_by('-created_at').exclude(album_name__contains="_Singles").values('id','album_name','album_coverImage','album_description','album_price','artist_id')
        page = self.paginate_queryset(albums)
        if page is not None:
            for album_count in range(len(page)):
                artists = ArtistsModel.objects.filter(id=page[album_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[album_count]['artist_name'] = artist_name
                page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(album_id=page[album_count]['id'], user_FUI=userId).exists()
                if TracksModel.objects.filter(track_status=True, album_id=page[album_count]['id']).exists():
                    page[album_count]['noOfTracks'] = TracksModel.objects.filter(track_status=True, album_id=page[album_count]['id']).count()
                else:
                     page[album_count]['noOfTracks'] = 0
        return Response(page)

class TracksByAlbumIdViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
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
        userId = request.query_params['userId']
        albumId = request.query_params['albumId']
        tracks = self.queryset.filter(track_status=True, album_id=albumId).order_by('-created_at').values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artists = ArtistsModel.objects.filter(id=page[track_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):    
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                elif page[track_count]['artists_featuring'] != "":
                    artist_name = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[track_count]['artist_name'] = artist_name
                page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[track_count]['id'], user_FUI=userId).exists()
        return Response(page)

class GenresMobileViewSet(viewsets.ModelViewSet):

    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer
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
        genres = self.queryset.filter(genre_status=True).order_by('-created_at').values('id','genre_name','genre_description','genre_coverImage')
        page = self.paginate_queryset(genres)
        return Response(page)

class TracksByGenreIdViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
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
        userId = request.query_params['userId']
        genreId = request.query_params['genreId']
        tracks = self.queryset.filter(track_status=True, genre_id=genreId).order_by('-created_at').values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artists = ArtistsModel.objects.filter(id=page[track_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):    
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                elif page[track_count]['artists_featuring'] != "":
                    artist_name = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[track_count]['artist_name'] = artist_name
                page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[track_count]['id'], user_FUI=userId).exists()
        return Response(page)

class TracksMobileViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
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
        userId = request.query_params['userId']
        tracks = self.queryset.filter(track_status=True).order_by('-created_at').values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artists = ArtistsModel.objects.filter(id=page[track_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):    
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                elif page[track_count]['artists_featuring'] != "":
                    artist_name = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[track_count]['artist_name'] = artist_name
                page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[track_count]['id'], user_FUI=userId).exists()
        return Response(page)

class FavouritesByUserIdViewSet(viewsets.ModelViewSet):

    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        userId = request.query_params['userId']
        favouries = self.queryset.filter(user_FUI=userId).order_by('-created_at').values('id','track_id')
        page = self.paginate_queryset(favouries)
        if page is not None:
            for fav_count in range(len(page)):
                page[fav_count]['fav_id'] = page[fav_count]['id']
                track = TracksModel.objects.filter(track_status=True, id=page[fav_count]['track_id']).order_by('-created_at').values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI')
                for val in ['id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI']:
                    page[fav_count][val] = track[0][val]
                # page.append(track)
                artists = ArtistsModel.objects.filter(id=track[0]['artist_id'])
                # artist_name = ""
                # if artists.count() > 1:
                #     for artist_count in range(len(artists)):    
                #         artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                # elif track[0]['artists_featuring'] != "":
                #     artist_name = artist_name + " ft. " + track[0]['artists_featuring']
                # else:
                artist_name = artists.values('artist_name')[0]['artist_name']
                page[fav_count]['artist_name'] = artist_name
                page[fav_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[fav_count]['id'], user_FUI=userId).exists()
        return Response(page)

class PlayListsByUserIdViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListsModel.objects.all()
    serializer_class = PlayListsSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        userId = request.query_params['userId']
        playlist = self.queryset.filter(user_FUI=userId).order_by('-created_at').values('id','playlist_name','user_FUI')
        page = self.paginate_queryset(playlist)
        return Response(page)

class PlayListTracksByPlaylistIdViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListTracksModel.objects.all()
    serializer_class = PlayListsTracksSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        userId = request.query_params['userId']
        playlistId = request.query_params['playlistId']
        playlistTracks = self.queryset.filter(playlist_id=playlistId).order_by('-created_at').values('id','playlist_id','track_id')
        page = self.paginate_queryset(playlistTracks)
        if page is not None:
            for track_count in range(len(page)):
                page[track_count]['playlist_track_id'] = page[track_count]['id']
                tracks = TracksModel.objects.filter(id=page[track_count]['track_id']).order_by('-created_at').values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI')
                for val in ['id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id','encoder_FUI']:
                    page[track_count][val] = tracks[0][val]
                artists = ArtistsModel.objects.filter(id=page[track_count]['artist_id'])
                artist_name = ""
                if artists.count() > 1:
                    for artist_count in range(len(artists)):    
                        artist_name = artist_name + ", " + artists.values('artist_name')[artist_count]['artist_name']
                elif page[track_count]['artists_featuring'] != "":
                    artist_name = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
                    artist_name = artists.values('artist_name')[0]['artist_name']
                page[track_count]['artist_name'] = artist_name
                page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[track_count]['id'], user_FUI=userId).exists()
        return Response(page)