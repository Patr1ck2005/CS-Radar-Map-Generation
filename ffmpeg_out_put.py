import subprocess
import json

# 定义前景、背景视频和音乐的路径
fg_video_path = 'media/videos/cs_radar_chart/1080p60/PlayerRadarChart.mov'
bgm_path = 'music/Piano Fantasia - Song for Denise (Maxi version).mp3'
bg_video_path = 'bg/vecteezy_abstract-plexus-tech-background-with-glowing-blue-shiny_21050150~1.mp4'

# 调用 ffprobe 获取视频信息
def get_video_duration(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    info = json.loads(result.stdout)
    return float(info['format']['duration'])

# 获取前景视频的时长
foreground_duration = get_video_duration(fg_video_path)

# 背景视频循环播放并与前景视频叠加，使用 NVENC GPU 加速
subprocess.run([
    'ffmpeg', '-hwaccel', 'cuda', '-stream_loop', '-1', '-t', str(foreground_duration), '-i', bg_video_path,
    '-i', fg_video_path, '-filter_complex', '[0][1]overlay', '-c:v', 'h264_nvenc', '-shortest', 'temp_output_video.mp4'
])

# 背景音乐循环播放并与生成的视频合成，继续使用 NVENC
subprocess.run([
    'ffmpeg', '-i', 'temp_output_video.mp4', '-stream_loop', '-1', '-t', str(foreground_duration), '-i', bgm_path,
    '-c:v', 'copy', '-c:a', 'aac', '-shortest', 'final_output_video_with_music.mp4'
])

