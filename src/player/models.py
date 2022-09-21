from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.db import models
from core import validators
from django.core.mail import send_mail

def Artists_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Artists_Profile_Images', str(instance.artist_name) + "_" + str(filename)])
    
def Albums_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Albums_Cover_Images', str(instance.album_name) + "_" + str(filename)])
    
def Genres_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Genres_Cover_Images', str(instance.genre_name) + "_" + str(filename)])

def Track_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Tracks_Cover_Images', str(instance.track_name) + "_" + str(filename)])

def Track_Files(instance, filename):
    return '/'.join(['Media_Files', 'Tracks_Audio_Files', str(instance.album_id), str(instance.track_name) + "_" + str(filename)])

class ArtistsModel(models.Model):

    class Meta:
        ordering = ['id']

    artist_name = models.CharField(null=False, blank=True, max_length=256)
    artist_title = models.CharField(null=True, blank=True, max_length=256)
    artist_rating = models.IntegerField(null=True, blank=True, default=0)
    artist_status = models.BooleanField(null=False, blank=True, default=False)
    artist_description = models.CharField(null=True, blank=True, max_length=4096)
    artist_viewcount = models.IntegerField(null=False, blank=True, default=0)
    artist_profileImage = models.ImageField(null=False, blank=True, upload_to=Artists_Profile_Images, validators=[validators.validate_image_extension])
    artist_FUI = models.CharField(null=False, blank=True, unique=True, max_length=1023)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.artist_name}"

class AlbumsModel(models.Model):

    class Meta:
        ordering = ['id']

    album_name = models.CharField(null=False, blank=True, max_length=256)
    album_rating = models.IntegerField(null=True, blank=True, default=0)
    album_status = models.BooleanField(null=False, blank=True, default=False)
    album_releaseDate = models.DateField(null=True, blank=True)
    album_description = models.CharField(null=True, blank=True, max_length=4096)
    album_viewcount = models.IntegerField(null=False, blank=True, default=0)
    album_coverImage = models.ImageField(null=False, blank=True, upload_to=Albums_Cover_Images, validators=[validators.validate_image_extension])
    album_price = models.IntegerField(null=False, blank=True, default=40)
    artist_id = models.ManyToManyField(ArtistsModel)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.album_name}"

class GenresModel(models.Model):

    class Meta:
        ordering = ['id']

    genre_name = models.CharField(null=False, blank=True, max_length=256)
    genre_rating = models.IntegerField(null=True, blank=True, default=0)
    genre_status = models.BooleanField(null=False, blank=True, default=False)
    genre_description = models.CharField(null=True, blank=True, max_length=4096)
    genre_viewcount = models.IntegerField(null=False, blank=True, default=0)
    genre_coverImage = models.ImageField(null=False, blank=True, upload_to=Genres_Cover_Images, validators=[validators.validate_image_extension])
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.genre_name}"

class TracksModel(models.Model):

    class Meta:
        ordering = ['id']

    track_name = models.CharField(null=False, blank=True, max_length=256)
    track_rating = models.IntegerField(null=True, blank=True, default=0)
    track_status = models.BooleanField(null=False, blank=True, default=False)
    track_releaseDate = models.DateField(null=True, blank=True)
    track_description = models.CharField(null=True, blank=True, max_length=4096)
    track_viewcount = models.IntegerField(null=False, blank=True, default=0)
    track_coverImage = models.ImageField(null=False, blank=True, upload_to=Track_Cover_Images, validators=[validators.validate_image_extension])
    track_audioFile = models.FileField(null=False, blank=True, upload_to=Track_Files, validators=[validators.validate_track_extension])
    track_lyrics = models.CharField(null=True, blank=True, max_length=4096)
    track_price = models.IntegerField(null=False, blank=True, default=5)
    artists_featuring = models.CharField(null=False, blank=True, max_length=256)
    artist_id = models.ManyToManyField(ArtistsModel)
    album_id = models.ForeignKey(AlbumsModel, null=False, blank=True, on_delete=models.DO_NOTHING)
    genre_id = models.ForeignKey(GenresModel, null=False, blank=True, on_delete=models.DO_NOTHING)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.track_name}"

class PlayListsModel(models.Model):

    class Meta:
        ordering = ['id']

    playlist_name = models.CharField(null=False, blank=True, max_length=256)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.playlist_name}"

class PlayListTracksModel(models.Model):

    class Meta:
        ordering = ['id']

    playlist_id = models.ForeignKey(PlayListsModel, null=False, blank=True, on_delete=models.CASCADE)
    track_id = models.ForeignKey(TracksModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.playlist_id}"

class FavouritesModel(models.Model):

    class Meta:
        ordering = ['id']

    track_id = models.ForeignKey(TracksModel, null=False, blank=True, on_delete=models.CASCADE)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class PurchasedTracksModel(models.Model):

    class Meta:
        ordering = ['id']

    track_id = models.IntegerField(null=False, blank=True)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class PurchasedAlbumsModel(models.Model):

    class Meta:
        ordering = ['id']

    album_id = models.IntegerField(null=False, blank=True)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)