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
class AlbumsByArtistIdViewSet(viewsets.ModelViewSet):

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
        artistId = request.query_params['artistId']
        indexOfcomma = 0
        startOfno = 0
        artist_id_list = []
        data = []

        # Slice all the artist id from query params using the ', ' operator and append the ids to the artistidlist
        for i in range(len(artistId)):
            if artistId[i] == ',':
                indexOfcomma = i
                artist_id_list.append(int(artistId[startOfno:indexOfcomma]))
                startOfno = indexOfcomma + 1
        artist_id_list.append(int(artistId[startOfno:]))
        albums = self.queryset.filter(artist_id__in=artist_id_list).values('id','album_name')

        # Count how many times an album is repeated with diffrent artist_id
        tmp_data = []
        for i in range(len(albums)):
            tmpvalue = albums[i]['id']
            count = 0
            for j in range(len(albums)):
                if tmpvalue == albums[j]['id']:
                    count = count + 1
            if count == len(artist_id_list):
                for k in range(len(albums)):
                    if albums[k]['id'] == tmpvalue:
                        if albums[k] not in tmp_data:
                            tmp_data.append(albums[k])

        # Check if the listed albums in the tmp_data only have artist ids of the requested artist ids   
        for i in range(len(tmp_data)):
            artist_obj = self.queryset.filter(id=tmp_data[i]['id']).values('id','album_name','artist_id')
            if len(artist_id_list) == len(artist_obj):
                data.append(tmp_data[i])

        return Response(data)

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

class PurchasedTracksWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedTracksModel.objects.all()
    serializer_class  = PurchasedTracksSerializer

class PurchasedAlbumsWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedAlbumsModel.objects.all()
    serializer_class = PurchasedAlbumsSerializer
    pagination_class = StandardResultsSetPagination