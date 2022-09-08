from rest_framework.routers import DefaultRouter

from player.mobile_app import *

router = DefaultRouter(trailing_slash=False)

router.register(r'data_by_userid', DataByUserId, basename="databyuserid")
router.register(r'popular_tracks', PopularMusicViewSet, basename="popular_tracks")
router.register(r'tracks', TracksViewSet, basename="tracks")
router.register(r'albums', ALbumsViewSet, basename="albums")
router.register(r'artists', ArtistsViewSet, basename="artists")
router.register(r'genres', GenresViewSet, basename="genres")