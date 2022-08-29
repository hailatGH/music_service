from django.contrib import admin

from .models import ArtistModel, AlbumModel, TrackModel, GenreModel, LyricsModel, PlayListModel, PlayListTracksModel, FavouritesModel

admin.site.register(ArtistModel)
admin.site.register(AlbumModel)
admin.site.register(GenreModel)
admin.site.register(TrackModel)
admin.site.register(LyricsModel)
admin.site.register(PlayListModel)
admin.site.register(PlayListTracksModel)
admin.site.register(FavouritesModel)