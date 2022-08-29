# Generated by Django 4.1 on 2022-08-29 18:30

import core.validators
from django.db import migrations, models
import django.db.models.deletion
import player.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_title', models.CharField(blank=True, max_length=100, unique=True)),
                ('album_cover', models.ImageField(blank=True, upload_to=player.models.Albums_Cover_Images, validators=[core.validators.validate_image_extension])),
                ('album_description', models.TextField(blank=True, null=True)),
                ('user_id', models.CharField(max_length=1023)),
                ('album_price', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ArtistModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(blank=True, max_length=100, unique=True)),
                ('artist_title', models.CharField(blank=True, max_length=100)),
                ('artist_cover', models.ImageField(blank=True, upload_to=player.models.Artists_Profile_Images, validators=[core.validators.validate_image_extension])),
                ('artist_description', models.TextField(blank=True, null=True)),
                ('user_id', models.CharField(max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GenreModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_title', models.CharField(blank=True, max_length=100, unique=True)),
                ('genre_cover', models.ImageField(blank=True, upload_to=player.models.Genres_Cover_Images, validators=[core.validators.validate_image_extension])),
                ('genre_description', models.TextField(blank=True, null=True)),
                ('user_id', models.CharField(max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PlayListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(blank=True, max_length=100)),
                ('user_id', models.CharField(max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TrackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(blank=True, max_length=100, unique=True)),
                ('track_description', models.TextField(blank=True, null=True)),
                ('track_file', models.FileField(blank=True, upload_to=player.models.Track_Files, validators=[core.validators.validate_track_extension])),
                ('track_status', models.BooleanField(default=False)),
                ('track_release_date', models.DateTimeField()),
                ('user_id', models.CharField(max_length=1023)),
                ('track_price', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks_al', to='player.albummodel')),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks_ar', to='player.artistmodel')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks_g', to='player.genremodel')),
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
                ('playlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_na', to='player.playlistmodel')),
                ('track_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_t', to='player.trackmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LyricsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lyrics_title', models.CharField(blank=True, max_length=100, unique=True)),
                ('lyrics_detail', models.TextField(blank=True, max_length=4092, unique=True)),
                ('user_id', models.CharField(max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('track_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lyrics', to='player.trackmodel', unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FavouritesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=1023)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('track_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favouritelist', to='player.trackmodel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='albummodel',
            name='artist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='albums', to='player.artistmodel'),
        ),
    ]
