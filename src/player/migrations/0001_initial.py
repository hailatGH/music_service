# Generated by Django 4.1 on 2022-10-28 08:36

import core.validators
import datetime
from django.db import migrations, models
import django.db.models.deletion
import player.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCollectionNamesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_name', models.CharField(blank=True, max_length=256, unique=True)),
                ('encoder_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='AlbumsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(blank=True, max_length=256)),
                ('album_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('album_status', models.BooleanField(blank=True, default=False)),
                ('album_releaseDate', models.DateField(blank=True, default=datetime.date(2022, 10, 28), null=True)),
                ('album_description', models.CharField(blank=True, max_length=4096, null=True)),
                ('album_viewcount', models.IntegerField(blank=True, default=0)),
                ('album_coverImage', models.ImageField(blank=True, upload_to=player.models.Albums_Cover_Images, validators=[core.validators.validate_image_extension])),
                ('album_price', models.IntegerField(blank=True, default=40)),
                ('encoder_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ArtistsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(blank=True, max_length=256)),
                ('artist_title', models.CharField(blank=True, max_length=256, null=True)),
                ('artist_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('artist_status', models.BooleanField(blank=True, default=False)),
                ('artist_releaseDate', models.DateField(blank=True, default=datetime.date(2022, 10, 28), null=True)),
                ('artist_description', models.CharField(blank=True, max_length=4096, null=True)),
                ('artist_viewcount', models.IntegerField(blank=True, default=0)),
                ('artist_profileImage', models.ImageField(blank=True, upload_to=player.models.Artists_Profile_Images, validators=[core.validators.validate_image_extension])),
                ('artist_FUI', models.CharField(blank=True, max_length=1023, unique=True)),
                ('encoder_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GenresModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(blank=True, max_length=256)),
                ('genre_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('genre_status', models.BooleanField(blank=True, default=False)),
                ('genre_description', models.CharField(blank=True, max_length=4096, null=True)),
                ('genre_viewcount', models.IntegerField(blank=True, default=0)),
                ('genre_coverImage', models.ImageField(blank=True, upload_to=player.models.Genres_Cover_Images, validators=[core.validators.validate_image_extension])),
                ('encoder_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PlayListsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(blank=True, max_length=256)),
                ('user_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PurchasedAlbumsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.IntegerField(blank=True)),
                ('user_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PurchasedTracksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.IntegerField(blank=True)),
                ('user_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TracksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(blank=True, max_length=256)),
                ('track_rating', models.IntegerField(blank=True, default=0, null=True)),
                ('track_status', models.BooleanField(blank=True, default=False)),
                ('track_releaseDate', models.DateField(blank=True, default=datetime.date(2022, 10, 28), null=True)),
                ('track_description', models.CharField(blank=True, max_length=4096, null=True)),
                ('track_viewcount', models.IntegerField(blank=True, default=0)),
                ('track_coverImage', models.ImageField(blank=True, upload_to=player.models.Track_Cover_Images, validators=[core.validators.validate_image_extension])),
                ('track_audioFile', models.FileField(blank=True, upload_to=player.models.Track_Files, validators=[core.validators.validate_track_extension])),
                ('track_lyrics', models.CharField(blank=True, max_length=4096, null=True)),
                ('track_price', models.IntegerField(blank=True, default=5)),
                ('artists_featuring', models.CharField(blank=True, max_length=256)),
                ('encoder_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('album_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trackasalbum', related_query_name='trackasalbumquery', to='player.albumsmodel')),
                ('artist_id', models.ManyToManyField(related_name='trackasartist', related_query_name='trackasartistquery', to='player.artistsmodel')),
                ('genre_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='genre_tracks', related_query_name='genre_tracks', to='player.genresmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PlayListTracksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('playlist_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='player.playlistsmodel')),
                ('track_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.tracksmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FavouritesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_FUI', models.CharField(blank=True, max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('track_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='player.tracksmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='albumsmodel',
            name='artist_id',
            field=models.ManyToManyField(related_name='albumasartist', related_query_name='albumasartistquery', to='player.artistsmodel'),
        ),
        migrations.CreateModel(
            name='AdminCollectionTracksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='player.admincollectionnamesmodel')),
                ('track_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.tracksmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
