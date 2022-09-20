from dataclasses import field, fields
from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.mail import send_mail

from .models import *

class ArtistsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArtistsModel
        fields = '__all__'

    def create(self, validated_data):
        artist = super().create(validated_data)
        try:
            SingleAlbum = AlbumsModel(
                album_name="Singles",
                album_status=validated_data['artist_status'],
                album_releaseDate=datetime.now(),
                album_description=f"Contains all single musics of the {validated_data['artist_name']}!",
                album_coverImage=validated_data['artist_profileImage'],
                encoder_FUI=validated_data['encoder_FUI']
            )
            SingleAlbum.save()
            SingleAlbum.artist_id.add(artist)
        except BaseException as e:
            Subject = "Data Consistancy Problem"
            Email_Body = f"Error: {e}\n\nIssue: Singles album is not created for the artist: {validated_data['artist_name']}."
            Sender = 'kinideas.tech@gmail.com'
            Receiver = 'hailat.alx@gmail.com'

            send_mail(Subject, Email_Body, Sender, [Receiver], fail_silently=False,)
        return artist

class AlbumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlbumsModel
        fields = '__all__'

class GenresSerializer(serializers.ModelSerializer):

     class Meta:
        model = GenresModel
        fields = '__all__'

class TracksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TracksModel
        fields = '__all__'

class PlayListsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlayListsModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PlayListsModel.objects.all(),
                fields=['playlist_name', 'user_FUI']
            )
        ]

class PlayListsTracksSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayListTracksModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PlayListTracksModel.objects.all(),
                fields=['playlist_id', 'track_id']
            )
        ]

class FavouritesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavouritesModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=FavouritesModel.objects.all(),
                fields=['track_id', 'user_FUI']
            )
        ]

class PurchasedTracksSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedTracksModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PurchasedTracksModel.objects.all(),
                fields=['track_id', 'user_FUI']
            )
        ]

class PurchasedAlbumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedAlbumsModel
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=PurchasedAlbumsModel.objects.all(),
                fields=['album_id', 'user_FUI']
            )
        ]