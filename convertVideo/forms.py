from django import forms
from django.core.validators import FileExtensionValidator


class VideoForm(forms.Form):
    video_extensions = ['avi', 'mp4', 'wav', 'wmv', 'mpeg', 'mkv', 'gif', 'flv']
    file = forms.FileField(
        label='文件',
        validators=[FileExtensionValidator(video_extensions)]
    )

    audio = forms.BooleanField(
        required=False,
        label='包含原音频'
    )

