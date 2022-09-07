from rest_framework.routers import DefaultRouter

from player.viewset_mobile_app import *

router = DefaultRouter(trailing_slash=False)

# router.register(r'artistbyuserid', ArtistByUserId, basename="artistbyuserid")
# router.register(r'albumbyuserid', AlbumByUserId, basename="albumbyuserid")
# router.register(r'album', AlbumViewSet, basename="album")
# router.register(r'genre', GenreViewSet, basename="genre")
# router.register(r'track', TrackViewSet, basename="track")
# router.register(r'lyrics', LyricsViewSet, basename="lyrics")
# router.register(r'playlists', PlayListViewSet, basename="playlists")
# router.register(r'playlisttracks', PlayListTracksViewSet, basename="playlisttracks")
# router.register(r'favourites', FavouritesViewSet, basename="favourites")