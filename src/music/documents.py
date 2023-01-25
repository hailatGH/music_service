from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer


from .models import AlbumsModel,  ArtistsModel, TracksModel, GenresModel

# ***************************************************************************
# ***************************************************************************
# *****************************       ***************************************
############################## ARTIST#######################################
# *****************************       ***************************************
# ***************************************************************************
# ***************************************************************************

my_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=1, max_gram=20),
    filter=['lowercase']
)

@registry.register_document
class MusicartistDocument(Document):

    trackasartist = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "track_name": fields.TextField(analyzer=my_analyzer),
        "track_description": fields.TextField(analyzer=my_analyzer),
        "track_status": fields.BooleanField(),
        "track_lyrics": fields.TextField(analyzer=my_analyzer),
        "encoder_FUI": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )

    albumasartist = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "album_name": fields.TextField(analyzer=my_analyzer),
        "album_description": fields.TextField(analyzer=my_analyzer),
        "album_status": fields.BooleanField(),
        "encoder_FUI": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }

    )
    artist_name=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })
    artist_description=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })

    def prepare_trackasartist(self, instance):
        return instance.get_artisttracks_for_es()

    def prepare_albumasartist(self, instance):
        return instance.get_artistalbums_for_es()

    class Index:
        name = "music_artist"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = ArtistsModel
        related_models = [AlbumsModel, TracksModel]

        fields = [
            "id",
            #"artist_name",
            "artist_title",
            "artist_rating",
            "artist_releaseDate",
            "artist_status",
            #"artist_description",
            "artist_viewcount",
            "artist_profileImage",
            "artist_FUI",
            "encoder_FUI",
            "created_at",
            "updated_at",

        ]

    def get_instances_from_related(self, related_instance):

        if isinstance(related_instance, AlbumsModel):
            return related_instance.artist_id.all()
        elif isinstance(related_instance, TracksModel):
            return related_instance.artist_id.all()
# ***************************************************************************
# ***************************************************************************
# *****************************       ***************************************
############################## ALBUM#######################################
# *****************************       ***************************************
# ***************************************************************************
# ***************************************************************************


@registry.register_document
class MusicalbumDocument(Document):

    trackasalbum = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "track_name": fields.TextField(analyzer=my_analyzer),
        "track_description": fields.TextField(analyzer=my_analyzer),
        "track_status": fields.BooleanField(),
        "track_lyrics": fields.TextField(analyzer=my_analyzer),
        "encoder_FUI": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )
    artist_id = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "artist_name": fields.TextField(analyzer=my_analyzer),
        "artist_title": fields.TextField(),
        "artist_description": fields.TextField(analyzer=my_analyzer),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )
    album_name=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })
    album_description=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })

    # def prepare_album_tracks(self, instance):
    #     return instance.get_albumtracks_for_es()

    class Index:
        name = "music_album"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = AlbumsModel
        related_models = [ArtistsModel, TracksModel]

        fields = [
            "id",
            #"album_name",
            "album_rating",
            "album_status",
            "album_releaseDate",
            #"album_description",
            "album_viewcount",
            "album_coverImage",
            "album_price",
            "encoder_FUI",
            "created_at",
            "updated_at",
            # "artist_id",
        ]

    def get_instances_from_related(self, related_instance):

        if isinstance(related_instance, ArtistsModel):
            return related_instance.albumasartist.all()
        elif isinstance(related_instance, TracksModel):
            return related_instance.album_id
# ***************************************************************************
# ***************************************************************************
# *****************************       ***************************************
############################## TRACK#######################################
# *****************************       ***************************************
# ***************************************************************************
# ***************************************************************************


@registry.register_document
class MusictrackDocument(Document):
    album_id = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "album_name": fields.TextField(analyzer=my_analyzer),
        "album_description": fields.TextField(analyzer=my_analyzer),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )
    genre_id = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "genre_name": fields.TextField(),
        "genre_description": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )
    artist_id = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "artist_name": fields.TextField(analyzer=my_analyzer),
        "artist_title": fields.TextField(),
        "artist_description": fields.TextField(analyzer=my_analyzer),
        "artist_FUI": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }
    )
    track_name=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })
    track_description=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })

    class Index:
        name = "music_track"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = TracksModel

        related_models = [AlbumsModel, ArtistsModel, GenresModel,]

        fields = [
            "id",
            #"track_name",
            "track_rating",
            "track_status",
            "track_releaseDate",
            #"track_description",
            "track_viewcount",
            "track_coverImage",
            "track_audioFile",
            "track_lyrics",
            "track_price",
            "artists_featuring",
            "encoder_FUI",
            "created_at",
            "updated_at",
            # "artist_id",
            # "album_id",
            # "genre_id",

        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ArtistsModel):
            return related_instance.trackasartist.all()
        elif isinstance(related_instance, AlbumsModel):
            return related_instance.trackasalbum.all()
        elif isinstance(related_instance, GenresModel):
            return related_instance.genre_tracks.all()
# ***************************************************************************
# ***************************************************************************
# *****************************       ***************************************
############################## GENRE#######################################
# *****************************       ***************************************
# ***************************************************************************
# ***************************************************************************


@registry.register_document
class MusicgenreDocument(Document):
    genre_tracks = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "track_name": fields.TextField(analyzer=my_analyzer),
        "track_description": fields.TextField(analyzer=my_analyzer),
        "track_status": fields.BooleanField(),
        "track_lyrics": fields.TextField(analyzer=my_analyzer),
        "encoder_FUI": fields.TextField(),
        "created_at": fields.DateField(),
        "updated_at": fields.DateField(),
    }

    )
    genre_name=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })
    genre_description=fields.TextField(analyzer=my_analyzer,fields={
            'raw': fields.TextField(analyzer='keyword'),
        })

    class Index:
        name = "music_genre"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = GenresModel
        related_models = [TracksModel,]
        fields = [
            "id",
            # "genre_name",
            "genre_rating",
            "genre_status",
            # "genre_description",
            "genre_viewcount",
            "genre_coverImage",
            "encoder_FUI",
            "created_at",
            "updated_at",

        ]

    def get_instances_from_related(self, related_instance):

        if isinstance(related_instance, TracksModel):
            return related_instance.genre_id


# @registry.register_document
# class PurchasedTracksModelDocument(Document):
#     track_id: fields.TextField()
#     def prepare_track_id(self, instance):
#         return instance.get_passtrackid_for_es()

#     class Index:
#         name = "music_purchasedtracks"
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }


#     class Django:
#         model = PurchasedTracksModel


#         fields = [
#             "id",
#             "track_id",
#             "user_FUI",

#         ]

# @registry.register_document
# class PurchasedAlbumsModelDocument(Document):
#     album_id: fields.TextField()
#     def prepare_album_id(self, instance):
#         return instance.get_passalbumid_for_es()

#     class Index:
#         name = "music_purchasedalbums"
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }


#     class Django:
#         model = PurchasedAlbumsModel

#         fields = [
#             "id",
#             "album_id",
#             "user_FUI",

#         ]
# python manage.py search_index --rebuild
# python manage.py inspectdb > index_models.py
