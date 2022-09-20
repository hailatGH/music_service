from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

# Standard Results Set Pagination 
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

# Class based model viewsets for the Web App
class ArtistsWebViewSet(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer
    pagination_class = StandardResultsSetPagination

class AlbumsWebViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
    pagination_class = StandardResultsSetPagination

class GenresWebViewSet(viewsets.ModelViewSet):
    
    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer
    pagination_class = StandardResultsSetPagination

class TracksWebViewSet(viewsets.ModelViewSet):
    
    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
    pagination_class = StandardResultsSetPagination

class PlayListsWebViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListsModel.objects.all()
    serializer_class = PlayListsSerializer
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

class PlayListTracksWebViewSet(viewsets.ModelViewSet):
    
    queryset = PlayListTracksModel.objects.all()
    serializer_class = PlayListsTracksSerializer
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

# class FavouritesWebViewSet(viewsets.ModelViewSet):

#     queryset = FavouritesModel.objects.all()
#     serializer_class = FavouritesSerializer
#     pagination_class = StandardResultsSetPagination

#     def create(self, request, *args, **kwargs):
#         return Response("Not Allowed")

#     def retrieve(self, request, *args, **kwargs):
#         return Response("Not Allowed")

#     def update(self, request, *args, **kwargs):
#         return Response("Not Allowed")

#     def partial_update(self, request, *args, **kwargs):
#         return Response("Not Allowed")

#     def destroy(self, request, *args, **kwargs):
#         return Response("Not Allowed")

class PurchasedTracksWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedTracksModel.objects.all()
    serializer_class  = PurchasedTracksSerializer

class PurchasedAlbumsWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedAlbumsModel.objects.all()
    serializer_class = PurchasedAlbumsSerializer
    pagination_class = StandardResultsSetPagination