from django.contrib import admin

from .models import *

admin.site.register(ArtistModel)
admin.site.register(AlbumModel)
admin.site.register(GenreModel)
admin.site.register(TrackModel)
admin.site.register(PlayListModel)
admin.site.register(PlayListTracksModel)
admin.site.register(FavouritesModel)
admin.site.register(PurchasedTrackModel)
admin.site.register(PurchasedAlbumModel)