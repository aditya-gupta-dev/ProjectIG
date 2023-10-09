import pytube
import os 
from threading import Thread
from moviepy.editor import VideoFileClip
from PIL import Image

#globals
threads = []

# loading urls

urls = []

# downloading videos
def download(url):    
    yt = pytube.YouTube(url)
    print(f'downloading {yt.video_id} started..')
    best_resolution = yt.streams.get_highest_resolution()
    best_resolution.download('videos')
    print(f'{yt.video_id} Done...')

for url in urls:
    thread = Thread(target=download, args=(url, ))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print('download complete')

#extracting frames from the video 

threads = []

def get_frame_from_video(name: str, frame: int = 15):
    return Image.fromarray(VideoFileClip(f'videos/{name}').get_frame(frame)).save(f'images/{name}.png')
    
names = os.listdir('videos')

for name in names:
    thread = Thread(target=get_frame_from_video, args=(name, ))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print('data loading completed..')