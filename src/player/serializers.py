from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.mail import send_mail

from .models import *

class FavouritesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavouritesModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=FavouritesModel.objects.all(),
                fields=['track_id', 'user_id']
            )
        ]

class PlayListTracksSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayListTracksModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PlayListTracksModel.objects.all(),
                fields=['playlist_id', 'track_id']
            )
        ]

class PlayListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlayListModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PlayListModel.objects.all(),
                fields=['playlist_name', 'user_id']
            )
        ]

class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackModel
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):

     class Meta:
        model = GenreModel
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumModel
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArtistModel
        fields = '__all__'

    def create(self, validated_data):
        artist = super().create(validated_data)
        try:
            AlbumModel.objects.create(album_title="Singles", album_cover=validated_data['artist_cover'], album_description="Contains all single musics of the Artist!", artist_id=artist, created_by=validated_data['created_by'])
        except BaseException as e:
            Subject = "Data Consistancy Problem"
            Email_Body = f"Error: {e}\n\nIssue: Singles album is not created for the artist {validated_data['artist_cover']}."
            Sender = 'kinideas.tech@gmail.com'
            Receiver = 'hailat.alx@gmail.com'

            send_mail(Subject, Email_Body, Sender, [Receiver], fail_silently=False,)
        return artist

class PurchasedTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedTrackModel
        fields = '__all__'

class PurchasedAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedAlbumModel
        fields = '__all__'