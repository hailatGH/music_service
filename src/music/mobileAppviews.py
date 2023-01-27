from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import requests
import json
from datetime import datetime

from .models import *
from .serializers import *
from .functions import *

# Standard Results Set Pagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# Class based model viewsets for the Mobile App


class ArtistIdByFUId(viewsets.ModelViewSet):

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
            userId = request.query_params['userId']
        except:
            userId = 1

        artist_obj = self.queryset.filter(
            artist_status=True, artist_FUI=userId)
        artist = []
        if artist_obj.exists():
            artist = artist_obj.values('id')
        return Response(artist)


class ArtistsByEncoderId(viewsets.ModelViewSet):

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
            userId = request.query_params['userId']
        except:
            userId = 1

        artists = self.queryset.filter(artist_status=True, encoder_FUI=userId).values(
            'id', 'artist_name', 'artist_profileImage', 'artist_description')
        page = []
        if artists.exists():
            page = self.paginate_queryset(artists)
        return Response(page)


class AlbumsByEncoderId(viewsets.ModelViewSet):

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
        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        albums = self.queryset.filter(album_status=True, encoder_FUI=userId).values(
            'id', 'album_name', 'album_coverImage', 'album_description')
        page = []
        if albums.exists():
            page = self.paginate_queryset(albums)
        return Response(page)


class TracksByEncoderId(viewsets.ModelViewSet):

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
        tracks = self.queryset.filter(track_status=True, encoder_FUI=userId).order_by(
            '-track_releaseDate').values('id', 'track_name', 'track_coverImage', 'track_description')
        page = []
        if tracks.exists():
            page = self.paginate_queryset(tracks)
        return Response(page)


class ArtistsMobileViewSet(viewsets.ModelViewSet):

    queryset = ArtistsModel.objects.all()
    serializer_class = ArtistsSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            paginated_response = paginateArtistResponse(
                response, page, pageSize)

        return Response(paginated_response)


class AlbumByArtistIdViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = int(request.query_params['userId'])
        except:
            userId = 1

        try:
            artistId = int(request.query_params['artistId'])
        except:
            artistId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if list_contains(data['artist_id'], artistId)]

            paginated_response = paginateAlbumResponse(
                filtered_response, page, pageSize, userId)

        return Response(paginated_response)


class TrackByArtistIdViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = int(request.query_params['userId'])
        except:
            userId = 1

        try:
            artistId = int(request.query_params['artistId'])
        except:
            artistId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in [pre_data for pre_data in response if not pre_data['album_id']] if list_contains(data['artist_id'], artistId)]

            paginated_response = paginateTrackResponse(
                filtered_response, page, pageSize, userId)

        return Response(paginated_response)


class AlbumsMobileViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = int(request.query_params['userId'])
        except:
            userId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            paginated_response = paginateAlbumResponse(
                response, page, pageSize, userId)

        return Response(paginated_response)


class TrackByAlbumIdViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        try:
            albumId = int(request.query_params['albumId'])
        except:
            albumId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if data['album_id'] == albumId]

            paginated_response = paginateTrackResponse(
                filtered_response, page, pageSize, userId)

        return Response(paginated_response)


class GenresMobileViewSet(viewsets.ModelViewSet):

    queryset = GenresModel.objects.all()
    serializer_class = GenresSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            paginated_response = paginateGenreResponse(
                response, page, pageSize)

        return Response(paginated_response)


class TrackByGenreIdViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        try:
            genreId = int(request.query_params['genreId'])
        except:
            genreId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if data['genre_id'] == genreId]

            paginated_response = paginateTrackResponse(
                filtered_response, page, pageSize, userId)

        return Response(paginated_response)


class TracksMobileViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            paginated_response = paginateTrackResponse(
                response, page, pageSize, userId)

        return Response(paginated_response)


class PopularTracksMobileViewSet(viewsets.ModelViewSet):

    queryset = TracksModel.objects.all()
    serializer_class = TracksSerializer

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
        pageSize = 15
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            sorted_response = multikeysort(
                response, ['-track_viewcount', 'track_releaseDate'])

            paginated_response = paginateTrackResponse(
                sorted_response, page, pageSize, userId)

        return Response(paginated_response)


class FavouritesByUserIdViewSet(viewsets.ModelViewSet):

    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer

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
        pageSize = 2
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if data['user_FUI'] == userId]
            fav_tracks = fetchTracksDetail(filtered_response, 'fav_id')
            paginated_response = paginateTrackResponse(
                fav_tracks, page, pageSize, userId)

        return Response(paginated_response)


class PlayListsByUserIdViewSet(viewsets.ModelViewSet):

    queryset = PlayListsModel.objects.all()
    serializer_class = PlayListsSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        user_FUI = request.data['user_FUI']

        # userExists = requests.get(f'http://0.0.0.0:8001/subscribedUsers/{user_FUI}')
        userExists = requests.get(
            f'https://kinideas-profile.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/subscribedUsers/{user_FUI}')
        if userExists.status_code == 200:
            expireDate = userExists.json()['subscription_expiry_date'].replace(
                "T", " ").replace("Z", "")
            now = str(datetime.now())[:len(expireDate)]
            if now <= expireDate:
                return super().create(request, *args, **kwargs)

        noOfPlaylists = self.queryset.filter(user_FUI=user_FUI).count()
        if noOfPlaylists < 100:
            return super().create(request, *args, **kwargs)

        return Response("Maximum number of playlists allowd to create for unsubscribed(expired subscription) users is 2!", status=status.HTTP_400_BAD_REQUEST)

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
        playlist = self.queryset.filter(user_FUI=userId).order_by(
            '-created_at').values('id', 'playlist_name', 'user_FUI')
        page = self.paginate_queryset(playlist)
        return Response(page)


class PlayListTracksByPlaylistIdViewSet(viewsets.ModelViewSet):

    queryset = PlayListTracksModel.objects.all()
    serializer_class = PlayListsTracksSerializer

    def create(self, request, *args, **kwargs):
        user_FUI = request.query_params['userId']
        playlistId = request.data['playlist_id']

        # userExists = requests.get(f'http://0.0.0.0:8001/subscribedUsers/{user_FUI}')
        userExists = requests.get(
            f'https://kinideas-profile.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/subscribedUsers/{user_FUI}')
        if userExists.status_code == 200:
            expireDate = userExists.json()['subscription_expiry_date'].replace(
                "T", " ").replace("Z", "")
            now = str(datetime.now())[:len(expireDate)]
            if now <= expireDate:
                return super().create(request, *args, **kwargs)

        noOfTracksInAPlaylist = self.queryset.filter(
            playlist_id=playlistId).count()
        if noOfTracksInAPlaylist < 100:
            return super().create(request, *args, **kwargs)

        return Response("Maximum number of tracks in a playlist allowd to create for unsubscribed(expired subscription) users is 10!", status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        pageSize = 2
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        try:
            playlistId = request.query_params['playlistId']
        except:
            playlistId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if data['playlist_id'] == int(playlistId)]

            playList_tracks = fetchTracksDetail(
                filtered_response, 'playlist_track_id')

            paginated_response = paginateTrackResponse(
                playList_tracks, page, pageSize, userId)

        return Response(paginated_response)


class PurchasedTracksMobileViewset(viewsets.ModelViewSet):

    queryset = PurchasedTracksModel.objects.all()
    serializer_class = PurchasedTracksSerializer

    def list(self, request, *args, **kwargs):
        pageSize = 2
        paginated_response = []

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        response = json.loads(json.dumps(
            super().list(request, *args, **kwargs).data))

        if response:
            filtered_response = [
                data for data in response if data['user_FUI'] == userId]

            purchased_track = fetchTracksDetail(
                filtered_response, 'purchasedTrack_id')

            paginated_response = paginateTrackResponse(
                purchased_track, page, pageSize, userId)

        return Response(paginated_response)


# class AdminCollectionNamesMobileViewSet(viewsets.ModelViewSet):

#     queryset = AdminCollectionNamesModel.objects.all()
#     serializer_class = AdminCollectionNamesSerializer
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

#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)


# class AdminCollectionTracksMobileViewSet(viewsets.ModelViewSet):

#     queryset = AdminCollectionTracksModel.objects.all()
#     serializer_class = AdminCollectionTracksSerializer
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

#     def list(self, request, *args, **kwargs):
#         userId = request.query_params['userId']
#         collectionId = request.query_params['collectionId']
#         tracks = self.queryset.filter(collection_id=collectionId).order_by(
#             '-created_at').values('id', 'collection_id', 'track_id')
#         page = []
#         if tracks.exists():
#             page = self.paginate_queryset(tracks)
#             if page is not None:
#                 for track_count in range(len(page)):
#                     page[track_count]['collection_track_id'] = page[track_count]['id']
#                     tracks = TracksModel.objects.filter(id=page[track_count]['track_id']).order_by('-created_at').values('id', 'track_name', 'track_description',
#                                                                                                                          'track_coverImage', 'track_audioFile', 'track_lyrics', 'track_price', 'artists_featuring', 'artist_id', 'album_id', 'genre_id', 'encoder_FUI')
#                     if tracks.exists():
#                         for val in ['id', 'track_name', 'track_description', 'track_coverImage', 'track_audioFile', 'track_lyrics', 'track_price', 'artists_featuring', 'artist_id', 'album_id', 'genre_id', 'encoder_FUI']:
#                             page[track_count][val] = tracks[0][val]
#                         artists = ArtistsModel.objects.filter(
#                             id=page[track_count]['artist_id'])
#                         artist_name = ""
#                         if artists.exists():
#                             if artists.count() > 1:
#                                 for artist_count in range(len(artists)):
#                                     artist_name = artist_name + ", " + \
#                                         artists.values('artist_name')[
#                                             artist_count]['artist_name']
#                             elif page[track_count]['artists_featuring'] != "":
#                                 artist_name = artist_name + " ft. " + \
#                                     page[track_count]['artists_featuring']
#                             else:
#                                 artist_name = artists.values('artist_name')[
#                                     0]['artist_name']
#                         page[track_count]['artist_name'] = artist_name
#                         page[track_count]['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(
#                             track_id=page[track_count]['id'], user_FUI=userId).exists()
#             return Response(page)
