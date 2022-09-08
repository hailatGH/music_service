from rest_framework.routers import DefaultRouter

from player.mobile_app import *

router = DefaultRouter(trailing_slash=False)

router.register(r'data_by_userid', DataByUserId, basename="databyuserid")
router.register(r'popular_tracks', PopularMusicViewSet, basename="popular_tracks")