from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.core.mail import send_mail
import json

from .models import *
from .serializers import *
from .functions import *

cdnUrl = "https://zemamultimediablobcdn.azureedge.net/zemacontainer/"

# Standard Results Set Pagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

# Class based model viewsets for the Web App


class ArtistsWebViewSet(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        try:
            url = "https://kinideas-profile.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/users"
            # url = "http://127.0.0.1:8000/users"
            data = {
                "user_id": request.data['artist_FUI'],
                "privilege": 2,
                "created_by": request.data['encoder_FUI']
            }
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}

            retry_strategy = Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS"],

            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.post(
                url, json=data, headers=headers)

            return super().create(request, *args, **kwargs)

        except BaseException as e:
            Subject = "Data Consistancy Problem"
            Email_Body = f"Error: {e}\n\nIssue: {request.data['artist_name']} with FUI {request.data['artist_FUI']} could not be created!"
            Sender = 'kinideas.tech@gmail.com'
            Receiver = 'hailat.alx@gmail.com'
            send_mail(Subject, Email_Body, Sender, [
                      Receiver], fail_silently=False,)

        return

    def update(self, request, *args, **kwargs):
        try:
            url = "https://kinideas-profile.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/users"
            # url = "http://127.0.0.1:8000/users"
            data = {
                "user_id": request.data['artist_FUI'],
                "privilege": 2,
                "created_by": request.data['encoder_FUI']
            }
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}

            retry_strategy = Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS"],

            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.post(
                url, json=data, headers=headers)

            return super().update(request, *args, **kwargs)

        except BaseException as e:
            Subject = "Data Consistancy Problem"
            Email_Body = f"Error: {e}\n\nIssue: {request.data['artist_name']} with FUI {request.data['artist_FUI']} could not be updated!"
            Sender = 'kinideas.tech@gmail.com'
            Receiver = 'hailat.alx@gmail.com'
            send_mail(Subject, Email_Body, Sender, [
                      Receiver], fail_silently=False,)

        return

    def destroy(self, request, *args, **kwargs):
        id = ArtistsModel.objects.filter(id=kwargs['pk']).values('artist_FUI')

        try:
            url = f"https://kinideas-profile.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/users/{id[0]['artist_FUI'] if id.exists() else 0}"
            # url = f"http://127.0.0.1:8000/users/{id[0]['artist_FUI'] if id.exists() else 0}"
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}

            retry_strategy = Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS"],

            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.delete(
                url, headers=headers)

            print(response.status_code)

            return super().destroy(request, *args, **kwargs)

        except BaseException as e:
            Subject = "Data Consistancy Problem"
            Email_Body = f"Error: {e}\n\nIssue: Artist with ID {kwargs['pk']} could not be deleted!"
            Sender = 'kinideas.tech@gmail.com'
            Receiver = 'hailat.alx@gmail.com'
            send_mail(Subject, Email_Body, Sender, [
                      Receiver], fail_silently=False,)

        return


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
        albums = self.queryset.filter(
            artist_id__in=artist_id_list).values()

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
            artist_obj = self.queryset.filter(id=tmp_data[i]['id']).values(
                'id', 'album_name', 'artist_id')
            if len(artist_id_list) == len(artist_obj):
                data.append(tmp_data[i])

        for item in data:
            item['album_coverImage'] = cdnUrl + item['album_coverImage']

        return Response(data)


class AlbumsWebViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
    pagination_class = StandardResultsSetPagination


class AlbumIdByAlbumNameWebViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        album_name = request.query_params['album_name']
        album_id = "No album with that name"
        album = self.queryset.filter(album_name=album_name).values('id')
        if album.exists():
            album_id = album[0]['id']
        return Response(album_id)


class AlbumsDetailWebViewSet(viewsets.ModelViewSet):

    queryset = AlbumDetailModel.objects.all()
    serializer_class = AlbumsDetailSerializer
    pagination_class = StandardResultsSetPagination


class GenresWebViewSet(viewsets.ModelViewSet):

    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer
    pagination_class = StandardResultsSetPagination


class TracksWebViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer
    pagination_class = StandardResultsSetPagination


class TracksDetailWebViewSet(viewsets.ModelViewSet):

    queryset = TrackDetailModel.objects.all()
    serializer_class = TracksDetailSerializer
    pagination_class = StandardResultsSetPagination


class ArtistShareOfAtrack(viewsets.ModelViewSet):

    queryset = TrackDetailModel.objects.all()
    serializer_class = TracksDetailSerializer

    def list(self, request, *args, **kwargs):
        trackId = int(request.query_params['trackId'])
        artistId = int(request.query_params['artistId'])
        totalArtists = self.queryset.filter(track_id=trackId)
        artistTrackCount = totalArtists.filter(
            artist_id=artistId)

        return Response(artistTrackCount.count()/totalArtists.count())


class ArtistShareOfAnAlbum(viewsets.ModelViewSet):

    queryset = AlbumDetailModel.objects.all()
    serializer_class = AlbumsDetailSerializer

    def list(self, request, *args, **kwargs):
        albumId = int(request.query_params['albumId'])
        artistId = int(request.query_params['artistId'])
        totalArtists = self.queryset.filter(album_id=albumId)
        artistTrackCount = totalArtists.filter(
            artist_id=artistId)

        return Response(artistTrackCount.count()/totalArtists.count())


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


class TracksViewCountWebViewSet(viewsets.ModelViewSet):

    queryset = TracksViewCount.objects.all()
    serializer_class = TracksViewCountSerializer
    pagination_class = StandardResultsSetPagination


class PurchasedTracksWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedTracksModel.objects.all()
    serializer_class = PurchasedTracksSerializer


class PurchasedAlbumsWebViewSet(viewsets.ModelViewSet):

    queryset = PurchasedAlbumsModel.objects.all()
    serializer_class = PurchasedAlbumsSerializer
    pagination_class = StandardResultsSetPagination

# class AdminCollectionNamesWebViewSet(viewsets.ModelViewSet):

#     queryset = AdminCollectionNamesModel.objects.all()
#     serializer_class = AdminCollectionNamesSerializer
#     pagination_class = StandardResultsSetPagination

# class AdminCollectionTracksWebViewSet(viewsets.ModelViewSet):

#     queryset = AdminCollectionTracksModel.objects.all()
#     serializer_class = AdminCollectionTracksSerializer
#     pagination_class = StandardResultsSetPagination


class FilterArtist(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        try:
            artistName = request.query_params['q']
        except:
            artistName = ""
        response = self.queryset.filter(
            artist_name__icontains=artistName).values('id', 'artist_name', 'artist_profileImage')
        for artist in response:
            artist['artist_profileImage'] = cdnUrl + \
                artist['artist_profileImage']

        return Response(response)


class FilterAlbum(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        try:
            albumName = request.query_params['q']
        except:
            albumName = ""
        response = self.queryset.filter(
            album_name__icontains=albumName).values('id', 'album_name', 'album_coverImage')
        for album in response:
            album['album_coverImage'] = cdnUrl + album['album_coverImage']

        return Response(response)


class FilterGenre(viewsets.ModelViewSet):

    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        try:
            genreName = request.query_params['q']
        except:
            genreName = ""
        response = self.queryset.filter(
            genre_name__icontains=genreName).values('id', 'genre_name', 'genre_coverImage')
        for genre in response:
            genre['genre_coverImage'] = cdnUrl + genre['genre_coverImage']

        return Response(response)


class ApprovedTracksCount(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        response = {}
        totalTrackCount = self.queryset.all().count()
        approvedTracks = self.queryset.filter(track_status=True).count()

        response["totalTrackCount"] = totalTrackCount
        response["approvedTracks"] = approvedTracks
        response["notApprovedTracks"] = totalTrackCount - approvedTracks
        return Response(response)


class GenreTracksCount(viewsets.ModelViewSet):

    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):

        response = self.queryset.all().values('id', 'genre_name')
        for genre in response:
            genre['trackCount'] = TracksModel.objects.filter(
                genre_id=genre['id']).count()

        return Response(response)


class ContentCount(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        response = {}
        response['tracksCount'] = TracksModel.objects.all().count()
        response['genresCount'] = GenresModel.objects.all().count()
        response['albumsCount'] = AlbumsModel.objects.all().count()
        response['artistsCount'] = ArtistsModel.objects.all().count()

        return Response(response)


class TopPopularTracks(viewsets.ModelViewSet):

    queryset = TracksViewCount.objects.all()
    serializer_class = TracksViewCountSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        response = []
        popularTracksList = TracksViewCount.objects.all().order_by(
            '-track_viewcount').values('track_id', 'track_viewcount')

        if popularTracksList.count() >= 10:
            for i in range(10):
                response.append(popularTracksList[i])
        else:
            response = popularTracksList

        response = fetchTracksDetail(response, "pop_id")

        return Response(response)
