from functools import cmp_to_key
from operator import itemgetter as i

from .models import *

cdnUrl = "https://zemamultimediablobcdn.azureedge.net/zemacontainer/"
# storageUrl = "http://127.0.0.1:8001/Media/"
storageUrl = "https://zemastroragev100.blob.core.windows.net/zemacontainer/"


def paginateArtistResponse(response, page, pageSize):
    paginated_response = []
    filtered_response = [
        data for data in response if data['artist_status']]

    indexEnd = (page * pageSize)
    indexStart = indexEnd - pageSize

    for val in filtered_response:
        index = filtered_response.index(val)
        if (index >= indexStart and index < indexEnd):
            paginated_response.append(filtered_response[index])

    for artist_count in range(len(paginated_response)):
        paginated_response[artist_count]['artist_profileImage'] = paginated_response[artist_count]['artist_profileImage'].replace(
            storageUrl, cdnUrl, 1)
        # try:
        #     paginated_response[artist_count]['noOfAlbums'] = AlbumsModel.objects.filter(
        #         album_status=True, artist_id=paginated_response[artist_count]['id']).count()
        # except:
        #     paginated_response[artist_count]['noOfAlbums'] = 0

        # try:
        #     paginated_response[artist_count]['noOfTracks'] = TracksModel.objects.filter(
        #         track_status=True, artist_id=paginated_response[artist_count]['id']).count()
        # except:
        #     paginated_response[artist_count]['noOfTracks'] = 0

    return paginated_response


def paginateAlbumResponse(response, page, pageSize, userId):
    paginated_response = []

    filtered_response = [
        data for data in response if data['album_status']]

    indexEnd = (page * pageSize)
    indexStart = indexEnd - pageSize

    for val in filtered_response:
        index = filtered_response.index(val)
        if (index >= indexStart and index < indexEnd):
            paginated_response.append(filtered_response[index])

    for album in paginated_response:
        artist_name = ""

        for id in album['artist_id']:
            privilege = AlbumDetailModel.objects.filter(
                album_id=album['id'], artist_id=id).values('artist_id', 'privilege')

            name = ArtistsModel.objects.filter(
                id=id).values('artist_name')[0]['artist_name']

            if privilege.exists():
                if privilege[0]['privilege'] == "Singer":
                    artist_name = artist_name + name + " x "
                else:
                    album[privilege[0]['privilege']] = name

        # artists = ArtistsModel.objects.filter(
        #     id__in=album['artist_id']).values('artist_name')
        # artist_name = ""

        # for artist in artists:
        #     artist_name = artist_name + artist['artist_name'] + " x "

        album['artist_name'] = artist_name[:len(artist_name) - 3]
        album['is_purchasedByUser'] = PurchasedAlbumsModel.objects.filter(
            album_id=album['id'], user_FUI=userId).exists()

        album['album_coverImage'] = album['album_coverImage'].replace(
            storageUrl, cdnUrl, 1)

    return paginated_response


def paginateGenreResponse(response, page, pageSize):
    paginated_response = []
    filtered_response = [
        data for data in response if data['genre_status']]

    indexEnd = (page * pageSize)
    indexStart = indexEnd - pageSize

    for val in filtered_response:
        index = filtered_response.index(val)
        if (index >= indexStart and index < indexEnd):
            paginated_response.append(filtered_response[index])

    for genre in paginated_response:
        genre['genre_coverImage'] = genre['genre_coverImage'].replace(
            storageUrl, cdnUrl, 1)

    return paginated_response


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
        artist_name = ""

        for id in track['artist_id']:
            privilege = TrackDetailModel.objects.filter(
                track_id=track['id'], artist_id=id).values('artist_id', 'privilege')

            name = ArtistsModel.objects.filter(
                id=id).values('artist_name')[0]['artist_name']

            if privilege.exists():
                if privilege[0]['privilege'] == "Singer":
                    artist_name = artist_name + name + " x "
                else:
                    track[privilege[0]['privilege']] = name

        track['artist_name'] = artist_name[:len(artist_name) - 3]
        track['is_purchasedByUser'] = PurchasedTracksModel.objects.filter(
            track_id=track['id'], user_FUI=userId).exists()

        track['track_coverImage'] = track['track_coverImage'].replace(
            storageUrl, cdnUrl, 1)
        track['track_audioFile'] = track['track_audioFile'].replace(
            storageUrl, cdnUrl, 1)

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
        track[0]['track_coverImage'] = cdnUrl + \
            track[0]['track_coverImage']
        track[0]['track_audioFile'] = cdnUrl + \
            track[0]['track_audioFile']
        track[0]['album_id'] = track[0].pop('album_id_id')
        track[0]['genre_id'] = track[0].pop('genre_id_id')
        track[0]['artist_id'] = artist_id
        tracks.append(track[0])

    return tracks
