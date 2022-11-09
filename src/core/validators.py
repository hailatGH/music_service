import os
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    if value is None:
        return
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename; [1] returns .extention
    valid_extensions = ['.jpg', '.png', '.jpeg'] # list of valid extentions for image
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension for an image!')

def validate_track_extension(value):
    # pass
    if value is None:
        return
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename; [1] returns .extention
    valid_extensions = ['.aac', '.mp3', '.wav'] # list of valid extentions for audio
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension for an audio file!')