from moviepy.editor import VideoFileClip, CompositeVideoClip
import config

def overlay_video(path: str, x: int, y: int, width: int, height: int):
    video1 = VideoFileClip(f'videos/{path}')
    overlay_template = VideoFileClip(config.noise_hider)
    resized_template = overlay_template.resize(height=height, width=width)
    final_video = CompositeVideoClip([video1.set_position((0, 0)).set_duration(video1.duration),
                                  resized_template.set_position((x, y)).set_duration(video1.duration)])
    
    final_video.write_videofile("output.mp4", threads=4, codec="libx264")

