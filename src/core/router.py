from rest_framework.routers import DefaultRouter

from music.webAppviews import *
from music.mobileAppviews import *

webApprouter = DefaultRouter(trailing_slash=False)
webApprouter.register(r'artist', ArtistsWebViewSet, basename="artist")
webApprouter.register(r'albumsByArtistId',
                      AlbumsByArtistIdViewSet, basename="albumsByArtistId")
webApprouter.register(r'albumIdByAlbumName',
                      AlbumIdByAlbumNameWebViewSet, basename="albumIdByAlbumName")
webApprouter.register(r'album', AlbumsWebViewSet, basename="album")
webApprouter.register(r'genre', GenresWebViewSet, basename="genre")
webApprouter.register(r'track', TracksWebViewSet, basename="track")
webApprouter.register(r'playlist', PlayListsWebViewSet, basename="playlist")
webApprouter.register(
    r'playlisttrack', PlayListTracksWebViewSet, basename="playlisttrack")
webApprouter.register(
    r'purchasedtrack', PurchasedTracksWebViewSet, basename="purchasedtrack")
webApprouter.register(
    r'purchasedalbum', PurchasedAlbumsWebViewSet, basename="purchasedalbum")
webApprouter.register(r'trackDetail',
                      TracksDetailWebViewSet, basename="trackDetail")
# webApprouter.register(r'adminCollectionName', AdminCollectionNamesWebViewSet, basename="adminCollectionName")
# webApprouter.register(r'adminCollectionTrack', AdminCollectionTracksWebViewSet, basename="adminCollectionTrack")

mobileApprouter = DefaultRouter(trailing_slash=False)
mobileApprouter.register(r'artists', ArtistsMobileViewSet, basename="artists")
mobileApprouter.register(
    r'albumByArtistId', AlbumByArtistIdViewSet, basename="albumByArtistId")
mobileApprouter.register(
    r'singleTracks', SingleTracksViewSet, basename="singleTracks")
mobileApprouter.register(r'albums', AlbumsMobileViewSet, basename="albums")
mobileApprouter.register(
    r'trackByAlbumId', TrackByAlbumIdViewSet, basename="trackByAlbumId")
mobileApprouter.register(r'genres', GenresMobileViewSet, basename="genres")
mobileApprouter.register(
    r'trackByGenreId', TrackByGenreIdViewSet, basename="trackByGenreId")
mobileApprouter.register(r'tracks', TracksMobileViewSet, basename="tracks")
mobileApprouter.register(
    r'popularTracks', PopularTracksMobileViewSet, basename="popularTracks")
mobileApprouter.register(
    r'favTracks', FavouritesByUserIdViewSet, basename="favTracks")
mobileApprouter.register(
    r'playlists', PlayListsByUserIdViewSet, basename="playlists")
mobileApprouter.register(
    r'tracksByPlaylistId', PlayListTracksByPlaylistIdViewSet, basename="tracksByPlaylistId")
mobileApprouter.register(r'purchasedTracksByUserId',
                         PurchasedTracksMobileViewset, basename="purchasedTracksByUserId")

mobileApprouter.register(
    r'artistIdByFUId', ArtistIdByFUId, basename="artistIdByFUId")
mobileApprouter.register(
    r'artistsByEncoderId', ArtistsByEncoderId, basename="artistsByEncoderId")
mobileApprouter.register(
    r'albumsByEncoderId', AlbumsByEncoderId, basename="albumsByEncoderId")
mobileApprouter.register(
    r'tracksByEncoderId', TracksByEncoderId, basename="tracksByEncoderId")
mobileApprouter.register(
    r'tracksByArtistId', TracksByArtistId, basename="tracksByArtistId")

# mobileApprouter.register(r'adminCollectionNames', AdminCollectionNamesMobileViewSet, basename="adminCollectionNames")
# mobileApprouter.register(r'adminCollectionTracks', AdminCollectionTracksMobileViewSet, basename="adminCollectionTracks")
