from django.db import models
from core import validators


def Artists_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Artists_Profile_Images', str(instance.artist_name) + "_" + str(filename)])
    
def Albums_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Albums_Cover_Images', str(instance.artist_id) + "_" + str(instance.album_title) + "_" + str(filename)])
    
def Genres_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Genres_Cover_Images', str(instance.genre_title) + "_" + str(filename)])
    
def Track_Files(instance, filename):
    return '/'.join(['Media_Files', 'Track_Files', str(instance.artist_id) + "_" + str(instance.album_id) + "_" + str(instance.track_name) + "_" + str(filename)])
    
class ArtistModel(models.Model):
    
    class Meta:
        ordering = ['id']

    artist_name = models.CharField(null=False, blank=True, unique=True, max_length=100)
    artist_title = models.CharField(null=False, blank=True, max_length=100)
    artist_cover = models.ImageField(upload_to=Artists_Profile_Images, validators=[validators.validate_image_extension], height_field=None, width_field=None, null=False, blank=True)
    artist_description = models.TextField(blank=True, null=True)
    user_id =  models.CharField(null=True, blank=True, max_length=1023)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d: %s' % (self.pk, self.artist_name)

class AlbumModel(models.Model):
    
    class Meta:
        ordering = ['id']

    album_title = models.CharField(null=False, blank=True, max_length=100)
    album_cover = models.ImageField(upload_to=Albums_Cover_Images, validators=[validators.validate_image_extension], height_field=None, width_field=None, null=False, blank=True)
    album_description = models.TextField(blank=True, null=True)
    artist_id = models.ForeignKey(ArtistModel, related_name='albums', on_delete=models.DO_NOTHING)
    album_price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.album_title)

class GenreModel(models.Model):

    class Meta:
        ordering = ['id']

    genre_title = models.CharField(null=False, blank=True, unique=True, max_length=100)
    genre_cover = models.ImageField(upload_to=Genres_Cover_Images, validators=[validators.validate_image_extension], height_field=None, width_field=None, null=False, blank=True)
    genre_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.genre_title)

class TrackModel(models.Model):
    
    class Meta:
        ordering = ['id']

    track_name = models.CharField(null=False, blank=True, unique=True, max_length=100)
    track_description = models.TextField(blank=True, null=True)
    track_file = models.FileField(upload_to=Track_Files, validators=[validators.validate_track_extension], null=False, blank=True)
    track_status = models.BooleanField(default=False)
    track_release_date=models.DateTimeField()
    artist_id = models.ForeignKey(ArtistModel, related_name='tracks_ar', on_delete=models.DO_NOTHING)
    album_id = models.ForeignKey(AlbumModel, related_name='tracks_al', on_delete=models.DO_NOTHING)
    genre_id = models.ForeignKey(GenreModel, related_name='tracks_g', on_delete=models.DO_NOTHING)
    track_price = models.IntegerField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.track_name)

class LyricsModel(models.Model):

    class Meta:
        ordering = ['id']

    lyrics_title = models.CharField(null=False, blank=True, unique=True, max_length=100)
    lyrics_detail = models.TextField(blank=True, null=False, unique=True, max_length=4092)
    track_id = models.ForeignKey(TrackModel, related_name='lyrics', on_delete=models.CASCADE, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.lyrics_title)

class PlayListModel(models.Model):

    class Meta:
        ordering = ['id']
    
    playlist_name = models.CharField(null=False, blank=True, max_length=100)
    user_id =  models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d: %s' % (self.pk, self.playlist_name)

class PlayListTracksModel(models.Model):

    class Meta:
        ordering = ['id']
    
    playlist_id = models.ForeignKey(PlayListModel, related_name='playlist_na', on_delete=models.CASCADE, null=False, blank=False)
    track_id = models.ForeignKey(TrackModel, related_name='playlist_t', on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d: %s' % (self.pk)

class FavouritesModel(models.Model):

    class Meta:
        ordering = ['id']
    
    track_id = models.ForeignKey(TrackModel, related_name='favouritelist', on_delete=models.CASCADE, null=False, blank=False)
    user_id =  models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d: %d' % (self.pk, self.user_id)