from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import AlbumModel, ArtistModel, TrackModel, GenreModel, LyricsModel, PlayListModel, PlayListTracksModel, FavouritesModel

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

class LyricsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LyricsModel
        fields = '__all__'

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
        AlbumModel.objects.create(album_title="Singles", album_cover=validated_data['artist_cover'], album_description="Contains all single musics of the Artist!", artist_id=artist)
        return artist