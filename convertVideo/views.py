import os
import shutil
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import VideoForm
from .task import cvt


def process_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['file']
            path = f'{settings.BASE_DIR}/convertVideo/cache/{datetime.now().strftime("%Y%m%d%H%M%S")}/'
            video_name = video_file.name
            os.makedirs(path)  # create cache
            with open(path + video_name, 'wb+') as f:
                f.write(video_file.read())

            converted = cvt(path, video_name)
            shutil.rmtree(path)  # clear cache
            if converted is not None:
                converted_name, converted_data = converted
                response = HttpResponse(converted_data, content_type='video/avi')
                response['Content-Disposition'] = f'attachment; filename={converted_name}'
                return response

    form = VideoForm()
    return render(request, 'convertVideo/upload.html', {'form': form})
