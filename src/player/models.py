import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.db import models
from core import validators

def Artists_Profile_Images(instance, filename):
    return '/'.join(['Media_Files', 'Artists_Profile_Images', str(instance.artist_name) + "_" + str(filename)])
    
def Albums_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Albums_Cover_Images', str(instance.artist_id) + "_" + str(instance.album_title) + "_" + str(filename)])
    
def Genres_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Genres_Cover_Images', str(instance.genre_title) + "_" + str(filename)])

def Track_Cover_Images(instance, filename):
    return '/'.join(['Media_Files', 'Track_Cover_Images', str(instance.track_name) + "_" + str(filename)])

def Track_Files(instance, filename):
    return '/'.join(['Media_Files', 'Track_Files', str(instance.artist_id), str(instance.album_id), str(instance.track_name) + "_" + str(filename)])
    
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
    user_id =  models.CharField(null=True, blank=True, max_length=1023)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.album_title)

    def save(self, *args, **kwargs):
        self.user_id = ArtistModel.objects.filter(id=int(str(self.artist_id)[slice(1)])).values('user_id')[0]['user_id']
        return super(AlbumModel, self).save(*args, **kwargs)

class GenreModel(models.Model):

    class Meta:
        ordering = ['id']

    genre_title = models.CharField(null=False, blank=True, unique=True, max_length=100)
    genre_cover = models.ImageField(upload_to=Genres_Cover_Images, validators=[validators.validate_image_extension], height_field=None, width_field=None, null=False, blank=True)
    genre_description = models.TextField(blank=True, null=True)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
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
    track_cover = models.ImageField(upload_to=Track_Cover_Images, validators=[validators.validate_image_extension], height_field=None, width_field=None, null=False, blank=True)
    track_status = models.BooleanField(default=False)
    track_release_date=models.DateTimeField()
    artist_id = models.ForeignKey(ArtistModel, related_name='tracks_ar', on_delete=models.DO_NOTHING)
    album_id = models.ForeignKey(AlbumModel, related_name='tracks_al', on_delete=models.DO_NOTHING)
    genre_id = models.ForeignKey(GenreModel, related_name='tracks_g', on_delete=models.DO_NOTHING)
    track_price = models.IntegerField(null=False, blank=True)
    user_id =  models.CharField(null=True, blank=True, max_length=1023)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
    viewcount = models.IntegerField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.track_name)

    def save(self, *args, **kwargs):
        self.user_id = ArtistModel.objects.filter(id=int(str(self.artist_id)[slice(1)])).values('user_id')[0]['user_id']
        respo = super(TrackModel, self).save(*args, **kwargs)
        try:
            # url = "http://127.0.0.1:8000/count/musicupdate"
            url = "https://analytics-service-v1-vdzflryflq-ew.a.run.app/count/musicupdate"
            data = {
                    "track_id": self.pk,
                    "album_id": int(str(self.album_id)[slice(1)]),
                    "artist_id": int(str(self.artist_id)[slice(1)]),
                    "user_id": self.user_id,
                    "created_by": self.created_by,
                }
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            
            retry_strategy = Retry(
                total=10, 
                backoff_factor=0.8, 
                status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            send_to_analytics = requests.post(url, json=data, headers=headers)
        except BaseException as e:
            with open("exceptions.txt", "a") as f:
                print(send_to_analytics, file=f)
                
        return respo

class LyricsModel(models.Model):

    class Meta:
        ordering = ['id']

    lyrics_title = models.CharField(null=False, blank=True, unique=True, max_length=100)
    lyrics_detail = models.TextField(blank=True, null=False, unique=True, max_length=4092)
    track_id = models.ForeignKey(TrackModel, related_name='lyrics', on_delete=models.CASCADE, unique=True)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%d: %s' % (self.pk, self.lyrics_title)

class PlayListModel(models.Model):

    class Meta:
        ordering = ['id']
    
    playlist_name = models.CharField(null=False, blank=True, max_length=100)
    created_by = models.CharField(null=False, blank=False, max_length=1023)
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
    created_by = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d: %d' % (self.pk, self.user_id)

class PurchasedTrackModel(models.Model):

    class Meta:
        ordering = ['id']
    
    track_id = models.IntegerField(null=False, blank=False)
    user_id = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PurchasedAlbumModel(models.Model):

    class Meta:
        ordering = ['id']
    
    album_id = models.IntegerField(null=False, blank=False)
    user_id = models.CharField(null=False, blank=False, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)