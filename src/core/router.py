from rest_framework.routers import DefaultRouter

from player.views import *

web_app_router = DefaultRouter(trailing_slash=False)
web_app_router.register(r'artist', ArtistViewSet, basename="artist")
web_app_router.register(r'album', AlbumViewSet, basename="album")
web_app_router.register(r'genre', GenreViewSet, basename="genre")
web_app_router.register(r'track', TrackViewSet, basename="track")
web_app_router.register(r'lyrics', LyricsViewSet, basename="lyrics")
web_app_router.register(r'playlists', PlayListViewSet, basename="playlists")
web_app_router.register(r'playlisttracks', PlayListTracksViewSet, basename="playlisttracks")
web_app_router.register(r'favourites', FavouritesViewSet, basename="favourites")
web_app_router.register(r'purchasedtrack', PurchasedTrackViewSet, basename="purchasedtrack")
web_app_router.register(r'purchasedalbum', PurchasedAlbumViewSet, basename="purchasedalbum")

mobile_app_router = DefaultRouter(trailing_slash=False)
# mobile_app_router.register(r'data_by_userid', DataByUserId, basename="databyuserid")
# mobile_app_router.register(r'popular_tracks', PopularMusicViewSet, basename="popular_tracks")
# mobile_app_router.register(r'tracks', TracksViewSet, basename="tracks")
# mobile_app_router.register(r'albums', ALbumsViewSet, basename="albums")
# mobile_app_router.register(r'artists', ArtistsViewSet, basename="artists")
# mobile_app_router.register(r'genres', GenresViewSet, basename="genres")