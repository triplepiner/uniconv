from moviepy.editor import *
#import cv2
import pytube
import ssl
import os
from pathlib import Path
import shutil

ssl._create_default_https_context = ssl._create_unverified_context




# Check whether the specified path exists or not


# if not isExist:
#
#     # Create a new directory because it does not exist
#     os.makedirs(path)
#     print("The new directory is created!")

def vid_to_gif(source,resize_factor,export):
    clip = VideoFileClip(source).resize(height=120)
    clip.write_gif(export)

def vid_to_avi(source,resize_factor,export):
    clip = VideoFileClip(source).resize (resize_factor)
    clip.write_videofile(export, codec='libx264')

def vid_to_mp4(source,resize_factor,export):
    clip = VideoFileClip(source).resize (resize_factor)
    clip.write_videofile(export, codec='libx264')

# def vid_to_imgs():
#     capture = cv2.VideoCapture (source)
#     frameNr = 0
#     dirName = path
#
#     while (True):
#         success, frame = capture.read ()
#         if success:
#             cv2.imwrite (f'{dirName}/{frameNr}.{export_format}', frame)
#         else:
#             break
#         frameNr = frameNr + 1
#
#     capture.release ()

# def imgs_to_vid():
#     images_list = f'output/'
#     clip = ImageSequenceClip(images_list, fps=25).resize(resize_factor)
#     clip.write_videofile(export_name +'.'+ export_format, codec='libx264')

def vid_to_audio(source,resize_factor,export):
    clip = VideoFileClip(source).resize(resize_factor)
    clip.audio.write_audiofile(export)


def yt_to_mp4(source,export):
    youtube = pytube.YouTube(source)
    video = youtube.streams.filter(file_extension='mp4').first()
    video.download (filename = f'{export}.mp4')

def yt_to_audio(source,export):
    youtube = pytube.YouTube(source)
    video = youtube.streams.filter(file_extension='mp4').first()
    video.download(filename='useless_file.mp4')
    mp4_file = 'useless_file.mp4'
    mp3_file = f'{export}.mp3'
    clip = AudioFileClip(mp4_file)
    clip.write_audiofile(mp3_file)
    os.remove(mp4_file)

def yt_videotitle(source):
    yt = pytube.YouTube(source)
    x = yt.streams[0].title
    return x

















