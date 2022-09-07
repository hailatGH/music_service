from time import clock_settime
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
class ArtistViewSet(viewsets.ModelViewSet):
    
    queryset = ArtistModel.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination

class AlbumViewSet(viewsets.ModelViewSet):
    
    queryset = AlbumModel.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = StandardResultsSetPagination
    
class GenreViewSet(viewsets.ModelViewSet):
    
    queryset = GenreModel.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination

class TrackViewSet(viewsets.ModelViewSet):
    
    queryset = TrackModel.objects.all()
    serializer_class = TrackSerializer
    pagination_class = StandardResultsSetPagination
        
class LyricsViewSet(viewsets.ModelViewSet):
    
    queryset = LyricsModel.objects.all()
    serializer_class = LyricsSerializer
    pagination_class = StandardResultsSetPagination

class PlayListViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListModel.objects.all()
    serializer_class = PlayListSerializer
    pagination_class = StandardResultsSetPagination

class PlayListTracksViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListTracksModel.objects.all()
    serializer_class = PlayListTracksSerializer
    pagination_class = StandardResultsSetPagination

class FavouritesViewSet(viewsets.ModelViewSet):

    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer
    pagination_class = StandardResultsSetPagination

class PurchasedTrackViewSet(viewsets.ModelViewSet):

    queryset = PurchasedTrackModel.objects.all()
    serializer_class  = PurchasedTrackSerializer

class PurchasedAlbumViewSet(viewsets.ModelViewSet):

    queryset = PurchasedAlbumModel.objects.all()
    serializer_class = PurchasedAlbumSerializer
    pagination_class = StandardResultsSetPagination