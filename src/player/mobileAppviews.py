from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

# Standard Results Set Pagination 
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
# Class based model viewsets for the Mobile App
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
        artists = self.queryset.order_by('-created_at').filter(artist_status=True).values('id','artist_name','artist_profileImage')
        page = self.paginate_queryset(artists)
        if page is not None:
            for artist_count in range(len(page)):
                albums = AlbumsModel.objects.filter(album_status=True, artist_id=page[artist_count]['id'])
                page[artist_count]['noOfAlbums'] = albums.count() - 1
                page[artist_count]['noOfTracks'] = TracksModel.objects.filter(track_status=False, album_id=albums.filter(album_name='Singles').values('id')[0]['id']).count()
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
        albums = self.queryset.order_by('-created_at').filter(album_status=True, artist_id=artistId).values('id','album_name','album_coverImage','album_description','album_price','artist_id')
        page = self.paginate_queryset(albums)
        if page is not None:
            for album_count in range(len(page)):
                artist_name = ArtistsModel.objects.filter(id=page[album_count]['artist_id']).values('artist_name')[0]['artist_name']
                page[album_count]['artist_name'] = artist_name
                page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(album_id=page[album_count]['id'], user_FUI=userId).exists()
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
        albums = self.queryset.order_by('-created_at').filter(album_status=True).exclude(album_name="Singles").values('id','album_name','album_coverImage','album_description','album_price','artist_id')
        page = self.paginate_queryset(albums)
        if page is not None:
            for album_count in range(len(page)):
                artist_name = ArtistsModel.objects.filter(id=page[album_count]['artist_id']).values('artist_name')[0]['artist_name']
                page[album_count]['artist_name'] = artist_name
                page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(album_id=page[album_count]['id'], user_FUI=userId).exists()
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
        tracks = self.queryset.order_by('-created_at').filter(track_status=False, album_id=albumId).values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artist_name = ArtistsModel.objects.filter(id=page[track_count]['artist_id']).values('artist_name')[0]['artist_name']
                if page[track_count]['artists_featuring'] != "":
                    page[track_count]['artist_name'] = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
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
        genres = self.queryset.order_by('-created_at').filter(genre_status=True).values('id','genre_name','genre_description','genre_coverImage')
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
        albumId = request.query_params['albumId']
        tracks = self.queryset.order_by('-created_at').filter(track_status=False, genre_id=albumId).values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artist_name = ArtistsModel.objects.filter(id=page[track_count]['artist_id']).values('artist_name')[0]['artist_name']
                if page[track_count]['artists_featuring'] != "":
                    page[track_count]['artist_name'] = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
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
        tracks = self.queryset.order_by('-created_at').filter(track_status=False).values('id','track_name','track_description','track_coverImage','track_audioFile','track_lyrics','track_price','artists_featuring','artist_id','album_id','genre_id')
        page = self.paginate_queryset(tracks)
        if page is not None:
            for track_count in range(len(page)):
                artist_name = ArtistsModel.objects.filter(id=page[track_count]['artist_id']).values('artist_name')[0]['artist_name']
                if page[track_count]['artists_featuring'] != "":
                    page[track_count]['artist_name'] = artist_name + " ft. " + page[track_count]['artists_featuring']
                else:
                    page[track_count]['artist_name'] = artist_name
                page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(track_id=page[track_count]['id'], user_FUI=userId).exists()
        return Response(page)