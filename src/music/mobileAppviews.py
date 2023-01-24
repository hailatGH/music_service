from functools import cmp_to_key
from operator import itemgetter as i
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import requests
import json
from datetime import datetime

from .models import *
from .serializers import *


def paginateTrackResponse(response, page, pageSize, userId):
    paginated_response = []

    filtered_response = [
        data for data in response if data['track_status']]

    indexEnd = (page * pageSize)
    indexStart = indexEnd - pageSize

    for val in filtered_response:
        index = filtered_response.index(val)
        if (index >= indexStart and index < indexEnd):
            paginated_response.append(filtered_response[index])

    for track in paginated_response:
        artists = ArtistsModel.objects.filter(
            id__in=track['artist_id']).values('artist_name')
        artist_name = ""

        for artist in artists:
            artist_name = artist_name + artist['artist_name'] + " x "

        track['artist_name'] = artist_name[:len(artist_name) - 3]
        track['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(
            track_id=track['id'], user_FUI=userId).exists()

    return paginated_response


def cmp(x, y):
    return (x > y) - (x < y)


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-')
         else (i(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def list_contains(List1, val):
    for item in List1:
        if item == val:
            print(item, end='')
            print(" - ", end='')
            print(val)
            return True
    return False


def fetchTracksDetail(filtered_response, kay_id):
    tracks = []

    for track_count in range(len(filtered_response)):
        track = TracksModel.objects.filter(
            id=filtered_response[track_count]['track_id']).values()
        artist_id = []
        for artist_count in range(len(track.values('artist_id'))):
            artist_id.append(track.values('artist_id')
                             [artist_count]['artist_id'])
        track = list(track)
        track[0][kay_id] = filtered_response[track_count]['id']
        track[0]['album_id'] = track[0].pop('album_id_id')
        track[0]['genre_id'] = track[0].pop('genre_id_id')
        track[0]['artist_id'] = artist_id
        tracks.append(track[0])

    return tracks

# Standard Results Set Pagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

# Class based model viewsets for the Mobile App


class ArtistIdByUserId(viewsets.ModelViewSet):

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
        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        artists = self.queryset.filter(artist_status=True, owner_FUI=userId).values(
            'id', 'artist_name', 'artist_profileImage', 'artist_description')
        page = []
        if artists.exists():
            page = self.paginate_queryset(artists)
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
        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        albums = self.queryset.filter(album_status=True, owner_FUI=userId).values(
            'id', 'album_name', 'album_coverImage', 'album_description')
        page = []
        if albums.exists():
            page = self.paginate_queryset(albums)
        return Response(page)


class TracksByArtistId(viewsets.ModelViewSet):

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
        pageSize = 3

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

        artistId = []
        artistId.append(userId)

        if response:
            filtered_response = [
                data for data in response if list_contains(data['artist_id'], int(userId))]

            paginated_response = paginateTrackResponse(
                filtered_response, page, pageSize, userId)

        return Response(paginated_response)


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
        artists = self.queryset.filter(artist_status=True).order_by(
            '-artist_rating').values('id', 'artist_name', 'artist_profileImage', 'artist_description')
        page = []
        if artists.exists():
            page = self.paginate_queryset(artists)
            if page is not None:
                for artist_count in range(len(page)):
                    albums = AlbumsModel.objects.filter(
                        album_status=True, artist_id=page[artist_count]['id'])
                    if albums.exists():
                        page[artist_count]['noOfAlbums'] = albums.count() - 1
                        tracks = TracksModel.objects.filter(
                            track_status=True, artist_id=page[artist_count]['id'])
                        if tracks.exists():
                            page[artist_count]['noOfTracks'] = tracks.count()
                        else:
                            page[artist_count]['noOfTracks'] = 0
                    else:
                        page[artist_count]['noOfAlbums'] = 0
                        page[artist_count]['noOfTracks'] = 0
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
        albums = self.queryset.filter(album_status=True, artist_id=artistId).order_by(
            '-album_rating').values('id', 'album_name', 'album_coverImage', 'album_description', 'album_price', 'artist_id')
        page = []
        if albums.exists():
            page = self.paginate_queryset(albums)
            if page is not None:
                for album_count in range(len(page)):
                    artists = ArtistsModel.objects.filter(
                        id=page[album_count]['artist_id'])
                    artist_name = ""
                    if artists.exists():
                        if artists.count() > 1:
                            for artist_count in range(len(artists)):
                                artist_name = artist_name + ", " + \
                                    artists.values('artist_name')[
                                        artist_count]['artist_name']
                        else:
                            artist_name = artists.values('artist_name')[
                                0]['artist_name']
                    page[album_count]['artist_name'] = artist_name
                    page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(
                        album_id=page[album_count]['id'], user_FUI=userId).exists()
                    tracks = TracksModel.objects.filter(
                        track_status=True, album_id=page[album_count]['id'])
                    if tracks.exists():
                        page[album_count]['noOfTracks'] = tracks.count()
                    else:
                        page[album_count]['noOfTracks'] = 0
        return Response(page)


class AlbumsMobileViewSet(viewsets.ModelViewSet):

    queryset = AlbumsModel.objects.all()
    serializer_class = AlbumsSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        return Response("Not Allowed")

    # def retrieve(self, request, *args, **kwargs):
    #     return Response("Not Allowed")

    def update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def partial_update(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        return Response("Not Allowed")

    def list(self, request, *args, **kwargs):
        userId = request.query_params['userId']
        albums = self.queryset.filter(album_status=True).order_by('-album_rating').exclude(album_name__contains="_Singles").values(
            'id', 'album_name', 'album_coverImage', 'album_description', 'album_price', 'artist_id')
        page = []
        if albums.exists():
            page = self.paginate_queryset(albums)
            if page is not None:
                for album_count in range(len(page)):
                    artists = ArtistsModel.objects.filter(
                        id=page[album_count]['artist_id'])
                    artist_name = ""
                    if artists.exists():
                        if artists.count() > 1:
                            for artist_count in range(len(artists)):
                                artist_name = artist_name + ", " + \
                                    artists.values('artist_name')[
                                        artist_count]['artist_name']
                        else:
                            artist_name = artists.values('artist_name')[
                                0]['artist_name']
                    page[album_count]['artist_name'] = artist_name
                    page[album_count]['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(
                        album_id=page[album_count]['id'], user_FUI=userId).exists()
                    tracks = TracksModel.objects.filter(
                        track_status=True, album_id=page[album_count]['id'])
                    if tracks.exists():
                        page[album_count]['noOfTracks'] = tracks.count()
                    else:
                        page[album_count]['noOfTracks'] = 0
        return Response(page)


class TracksByAlbumIdViewSet(viewsets.ModelViewSet):

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
        pageSize = 3

        try:
            page = int(request.query_params['page'])
        except:
            page = 1

        try:
            userId = request.query_params['userId']
        except:
            userId = 1

        try:
            albumId = request.query_params['albumId']
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
        genres = self.queryset.filter(genre_status=True).order_by(
            '-genre_rating').values('id', 'genre_name', 'genre_description', 'genre_coverImage')
        page = []
        if genres.exists():
            page = self.paginate_queryset(genres)
        return Response(page)


class TracksByGenreIdViewSet(viewsets.ModelViewSet):

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
        pageSize = 3

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
        pageSize = 3

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
        pageSize = 3

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
