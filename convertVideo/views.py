import os
import shutil
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import VideoForm, PreferenceForm
from .task import cvt


def upload_view(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['file']
            video_name = video_file.name

            format_choice = request.session.get('format_choice',
                                                PreferenceForm.initial_values['format_choice'])
            background_color = request.session.get('background_color',
                                                   PreferenceForm.initial_values['background_color'])
            char_color = request.session.get('char_color',
                                             PreferenceForm.initial_values['char_color'])
            refer_dimension = request.session.get('refer_dimension',
                                                  PreferenceForm.initial_values['refer_dimension'])
            char_number = request.session.get('char_number',
                                              PreferenceForm.initial_values['char_number'])
            audio = request.session.get('audio',
                                        PreferenceForm.initial_values['audio'])

            path = f'{settings.BASE_DIR}/convertVideo/cache/{datetime.now().strftime("%Y%m%d%H%M%S")}/'
            os.makedirs(path)  # create cache

            with open(path + video_name, 'wb+') as f:
                f.write(video_file.read())  # write the uploaded video to server's cache

            converted = cvt(path, video_name, format_choice, background_color, char_color,
                            refer_dimension, char_number, audio)
            shutil.rmtree(path)  # clear cache
            if converted is not None:
                converted_name, converted_data = converted
                response = HttpResponse(converted_data, content_type=f'video/{format_choice}')
                response['Content-Disposition'] = f'attachment; filename={converted_name}'
                return response

    form = VideoForm()
    return render(request, 'convertVideo/upload.html', {'VideoForm': form})


def preference_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['format_choice'] = form.cleaned_data['format_choice']
            request.session['background_color'] = form.cleaned_data['background_color']
            request.session['char_color'] = form.cleaned_data['char_color']
            request.session['refer_dimension'] = form.cleaned_data['refer_dimension']
            request.session['char_number'] = form.cleaned_data['char_number']
            request.session['audio'] = form.cleaned_data['audio']

            return render(request, 'convertVideo/preference.html', {'PreferenceForm': form})

    form = PreferenceForm(request.session)
    return render(request, 'convertVideo/preference.html', {'PreferenceForm': form})
