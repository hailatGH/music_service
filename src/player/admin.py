from django.contrib import admin

from .models import *

admin.site.register(ArtistsModel)
admin.site.register(AlbumsModel)
admin.site.register(GenresModel)
admin.site.register(TracksModel)
admin.site.register(PlayListsModel)
admin.site.register(PlayListTracksModel)
admin.site.register(FavouritesModel)
admin.site.register(PurchasedTracksModel)
admin.site.register(PurchasedAlbumsModel)