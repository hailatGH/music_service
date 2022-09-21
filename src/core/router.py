from rest_framework.routers import DefaultRouter

from player.webAppviews import *
from player.mobileAppviews import *

webApprouter = DefaultRouter(trailing_slash=False)
webApprouter.register(r'artist', ArtistsWebViewSet, basename="artist")
webApprouter.register(r'album', AlbumsWebViewSet, basename="album")
webApprouter.register(r'genre', GenresWebViewSet, basename="genre")
webApprouter.register(r'track', TracksWebViewSet, basename="track")
webApprouter.register(r'playlist', PlayListsWebViewSet, basename="playlist")
webApprouter.register(r'playlisttrack', PlayListTracksWebViewSet, basename="playlisttrack")
webApprouter.register(r'purchasedtrack', PurchasedTracksWebViewSet, basename="purchasedtrack")
webApprouter.register(r'purchasedalbum', PurchasedAlbumsWebViewSet, basename="purchasedalbum")

mobileApprouter = DefaultRouter(trailing_slash=False)
mobileApprouter.register(r'artists', ArtistsMobileViewSet, basename="artists")
mobileApprouter.register(r'albumsByArtistId', AlbumByArtistIdViewSet, basename="albumsByArtistId")
mobileApprouter.register(r'albums', AlbumsMobileViewSet, basename="albums")
mobileApprouter.register(r'tracksByAlbumId', TracksByAlbumIdViewSet, basename="tracksByAlbumId")
mobileApprouter.register(r'genres', GenresMobileViewSet, basename="genres")
mobileApprouter.register(r'tracksByGenreId', TracksByGenreIdViewSet, basename="tracksByGenreId")
mobileApprouter.register(r'tracks', TracksMobileViewSet, basename="tracks")
mobileApprouter.register(r'favTracks', FavouritesByUserIdViewSet, basename="favTracks")
mobileApprouter.register(r'playlists', PlayListsByUserIdViewSet, basename="playlists")
mobileApprouter.register(r'tracksByPlaylistId', PlayListTracksByPlaylistIdViewSet, basename="tracksByPlaylistId")