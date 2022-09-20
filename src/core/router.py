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
# mobile_app_router.register(r'data_by_userid', DataByUserId, basename="databyuserid")
# mobile_app_router.register(r'popular_tracks', PopularMusicViewSet, basename="popular_tracks")
# mobile_app_router.register(r'tracks', TracksViewSet, basename="tracks")
# mobile_app_router.register(r'albums', ALbumsViewSet, basename="albums")
# mobile_app_router.register(r'artists', ArtistsViewSet, basename="artists")
# mobile_app_router.register(r'genres', GenresViewSet, basename="genres")