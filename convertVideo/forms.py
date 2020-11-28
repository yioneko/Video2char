from django import forms
from django.core.validators import FileExtensionValidator


class VideoForm(forms.Form):
    video_extensions = ['avi', 'mp4', 'wmv', 'mpeg', 'mkv', 'gif', 'flv']
    file = forms.FileField(
        label='文件',
        validators=[FileExtensionValidator(video_extensions)]
    )


class PreferenceForm(forms.Form):
    video_format = ['mp4', 'avi', 'wmv', 'mkv']
    initial_values = {
        'format_choice': 'mp4',
        'background_color': '#FFFFFF',
        'char_color': '#000000',
        'refer_dimension': 'horizontal',
        'char_number': 100,
        'audio': False
    }

    format_choice = forms.ChoiceField(
        label='格式',
        choices=[(fmt, fmt) for fmt in video_format],
        initial=initial_values['format_choice']
    )

    background_color = forms.CharField(
        label='背景颜色',
        max_length=7,
        widget=forms.TextInput(attrs={'type': 'color'}),
        initial=initial_values['background_color']
    )

    char_color = forms.CharField(
        label='字符颜色',
        max_length=7,
        widget=forms.TextInput(attrs={'type': 'color'}),
        initial=initial_values['char_color']
    )

    refer_dimension = forms.ChoiceField(
        choices=[
            ('horizontal', '水平方向'),
            ('vertical', '垂直方向')
        ],
        initial=initial_values['refer_dimension']
    )

    char_number = forms.IntegerField(
        min_value=10,
        max_value=200,
        required=True,
        initial=initial_values['char_number']
    )

    audio = forms.BooleanField(
        required=False,
        label='包含原音频',
        initial=initial_values['audio']
    )
