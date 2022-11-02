from django.db import models
from core import validators
from django.utils import timezone
from django.core.files import File
from PIL import Image, ImageOps
from io import BytesIO

today = timezone.now()

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
    # artist_releaseDate = models.DateField(null=True, blank=True, default=timezone.now())
    artist_description = models.CharField(null=True, blank=True, max_length=4096)
    artist_viewcount = models.IntegerField(null=False, blank=True, default=0)
    artist_profileImage = models.ImageField(null=False, blank=True, upload_to=Artists_Profile_Images, validators=[validators.validate_image_extension])
    artist_FUI = models.CharField(null=False, blank=True, unique=True, max_length=1023)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    def get_artisttracks_for_es(self):
        tracks = self.trackasartist.all()
        artist_tracks_list = []
        for x in tracks:
            artist_tracks_list.append({'id':x.id,'track_name':x.track_name,'track_description':x.track_description,'track_status':x.track_status,'encoder_FUI':x.encoder_FUI,'created_at':x.created_at.date(),'updated_at':x.updated_at.date(),})
        return artist_tracks_list
    
    def get_artistalbums_for_es(self):
        albums = self.albumasartist.all()
        artist_albums_list = []
        for x in albums:
            artist_albums_list.append({'id':x.id,'album_name':x.album_name,'album_description':x.album_description,'album_status':x.album_status,'encoder_FUI':x.encoder_FUI,'created_at':x.created_at.date(),'updated_at':x.updated_at.date(),})
        return artist_albums_list
    
    def save(self, *args, **kwargs):
        image = Image.open(self.artist_profileImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(image_io, name=str(self.artist_profileImage))
        self.artist_profileImage = compressed_image
        super(ArtistsModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.artist_name}-{self.created_at.date()}/{self.updated_at.date()}"

class AlbumsModel(models.Model):

    class Meta:
        ordering = ['id']

    album_name = models.CharField(null=False, blank=True, max_length=256)
    album_rating = models.IntegerField(null=True, blank=True, default=0)
    album_status = models.BooleanField(null=False, blank=True, default=False)
    album_releaseDate = models.DateField(null=True, blank=True, default=today)
    album_description = models.CharField(null=True, blank=True, max_length=4096)
    album_viewcount = models.IntegerField(null=False, blank=True, default=0)
    album_coverImage = models.ImageField(null=False, blank=True, upload_to=Albums_Cover_Images, validators=[validators.validate_image_extension])
    album_price = models.IntegerField(null=False, blank=True, default=40)
    artist_id = models.ManyToManyField(ArtistsModel, related_name = "albumasartist", related_query_name= "albumasartistquery")
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.album_coverImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(image_io, name=str(self.album_coverImage))
        self.album_coverImage = compressed_image
        super(AlbumsModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.album_name}-{self.created_at.date()}/{self.updated_at.date()}"

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

    def save(self, *args, **kwargs):
        image = Image.open(self.genre_coverImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(image_io, name=str(self.genre_coverImage))
        self.genre_coverImage = compressed_image
        super(GenresModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.genre_name}-{self.created_at.date()}/{self.updated_at.date()}"

class TracksModel(models.Model):

    class Meta:
        ordering = ['id']

    track_name = models.CharField(null=False, blank=True, max_length=256)
    track_rating = models.IntegerField(null=True, blank=True, default=0)
    track_status = models.BooleanField(null=False, blank=True, default=False)
    track_releaseDate = models.DateField(null=True, blank=True, default=today)
    track_description = models.CharField(null=True, blank=True, max_length=4096)
    track_viewcount = models.IntegerField(null=False, blank=True, default=0)
    track_coverImage = models.ImageField(null=False, blank=True, upload_to=Track_Cover_Images, validators=[validators.validate_image_extension])
    track_audioFile = models.FileField(null=False, blank=True, upload_to=Track_Files, validators=[validators.validate_track_extension])
    track_lyrics = models.CharField(null=True, blank=True, max_length=4096)
    track_price = models.IntegerField(null=False, blank=True, default=5)
    artists_featuring = models.CharField(null=False, blank=True, max_length=256)
    artist_id = models.ManyToManyField(ArtistsModel, related_name = "trackasartist", related_query_name= "trackasartistquery")
    album_id = models.ForeignKey(AlbumsModel,related_name = "trackasalbum", related_query_name= "trackasalbumquery",null=False, blank=True, on_delete=models.DO_NOTHING)
    genre_id = models.ForeignKey(GenresModel, related_name = "genre_tracks",related_query_name= "genre_tracks", null=False, blank=True, on_delete=models.DO_NOTHING)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.track_coverImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(image_io, name=str(self.track_coverImage))
        self.track_coverImage = compressed_image
        super(TracksModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.track_name}-{self.created_at.date()}/{self.updated_at.date()}"

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
        return f"{self.pk}-{self.playlist_id}-{self.created_at.date()}/{self.updated_at.date()}"

class FavouritesModel(models.Model):

    class Meta:
        ordering = ['id']

    track_id = models.ForeignKey(TracksModel, null=False, blank=True, on_delete=models.CASCADE)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at.date()}/{self.updated_at.date()}"

class PurchasedTracksModel(models.Model):

    class Meta:
        ordering = ['id']

    track_id = models.IntegerField(null=False, blank=True)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at.date()}/{self.updated_at.date()}"

class PurchasedAlbumsModel(models.Model):

    class Meta:
        ordering = ['id']

    album_id = models.IntegerField(null=False, blank=True)
    user_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at.date()}/{self.updated_at.date()}"


class AdminCollectionNamesModel(models.Model):

    class Meta:
        ordering = ['id']

    collection_name = models.CharField(null=False, blank=True, max_length=256, unique=True)
    encoder_FUI = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.collection_name}"    

class AdminCollectionTracksModel(models.Model):

    class Meta:
        ordering = ['id']

    collection_id = models.ForeignKey(AdminCollectionNamesModel, null=False, blank=True, on_delete=models.CASCADE)
    track_id = models.ForeignKey(TracksModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)