from django import forms
from django.core.validators import FileExtensionValidator


class VideoForm(forms.Form):
    video_extensions = ['avi', 'mp4', 'wav', 'wmv', 'mpeg', 'mkv', 'gif']
    file = forms.FileField(
        required=True,
        label='文件',
        validators=[FileExtensionValidator(video_extensions)]
    )

