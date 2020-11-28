import cv2
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *


def frame2img(path, frame, cur, background_color, char_color,
              refer_dimension, char_number):
    chars = 'mqpka89045321@#$%^&*()_=||||}'

    original_height, original_width, channels = frame.shape

    width, height = get_char_number(refer_dimension, char_number,
                                    original_width, original_height)
    # number of chars on the horizontal and vertical direction

    frame = cv2.resize(frame, (width, height))

    char_text = ''
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for i in range(height):
        for j in range(width):
            gray_scale = gray[i, j]
            char = chars[int(gray_scale / 256 * len(chars))]
            char_text += char
        char_text += '\n'

    font_width, font_height = ImageFont.load_default().font.getsize(char_text[0])
    img = Image.new('RGB', (width * font_width, height * font_height), background_color)
    # reserve sufficient area to draw the text
    draw = ImageDraw.Draw(img)
    draw.multiline_text((0, 0), char_text, fill=char_color, spacing=0)
    img = img.resize((original_width, original_height))  # adjust the the original frame size
    img.save(f'{path}/{cur}.jpg')


def cvt(path, video_name, format_choice, background_color,
        char_color, refer_dimension, char_number, audio):
    converted_name = os.path.splitext(video_name)[0] + '_converted.' + format_choice

    video = cv2.VideoCapture(f'{path}/{video_name}')
    if video.isOpened():
        fps = video.get(cv2.CAP_PROP_FPS)
        ret, frame = video.read()
        size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        count = 0
        while ret:
            count += 1
            frame2img(path, frame, count, background_color, char_color,
                      refer_dimension, char_number)
            ret, frame = video.read()

        video_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        video_writer = cv2.VideoWriter(f'{path}/{converted_name}', video_fourcc, fps, size)

        for i in range(1, count + 1):
            img = cv2.imread(f'{path}/{i}.jpg')
            video_writer.write(img)
        video_writer.release()

        if audio:
            add_audio(path, video_name, converted_name, format_choice)

        with open(f'{path}/{converted_name}', 'rb') as f:
            file_data = f.read()  # return the binary data for transmission
        return converted_name, file_data


def add_audio(path, video_name, converted_name, format_choice):
    tmp_converted_name = f'{path}/converted_with_audio_temp.{format_choice}'

    video = VideoFileClip(f'{path}/{video_name}')
    converted_video = VideoFileClip(f'{path}/{converted_name}')
    audio = video.audio
    converted_video = converted_video.set_audio(audio)
    converted_video.write_videofile(tmp_converted_name)
    # write to the original file is not allowed

    video.close()
    converted_video.close()

    os.remove(f'{path}/{converted_name}')
    os.rename(tmp_converted_name, f'{path}/{converted_name}')


# get number of characters on the horizontal and
# vertical direction according to preference
def get_char_number(refer_dimension, char_number, width, height):
    assert refer_dimension in ['horizontal', 'vertical']

    if refer_dimension == 'vertical':
        return int(width / height * char_number), char_number
    elif refer_dimension == 'horizontal':
        return char_number, int(height / width * char_number)