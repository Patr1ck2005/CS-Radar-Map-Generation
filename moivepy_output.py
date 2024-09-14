from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips

fg_video_path = 'media/videos/cs_radar_chart/1080p60/PlayerRadarChart.mov'
bgm_path = 'music/Piano Fantasia - Song for Denise (Maxi version).mp3'
bg_video_path = 'bg/vecteezy_abstract-plexus-tech-background-with-glowing-blue-shiny_21050150~1.mp4'

# 加载前景视频（带透明度的 .mov 视频）
foreground = VideoFileClip(fg_video_path, has_mask=True)

# 加载背景视频并循环播放，确保背景视频长度与前景视频一致
background = VideoFileClip(bg_video_path).loop(duration=foreground.duration)

# 合成前景和背景视频，前景视频叠加到背景上
final_video = CompositeVideoClip([background, foreground])

# 加载背景音乐
audio = AudioFileClip(bgm_path)

# 手动循环音频以匹配前景视频时长
audio_clips = []
audio_duration = 0
while audio_duration < foreground.duration:
    audio_clips.append(audio)
    audio_duration += audio.duration

# 将所有音频片段连接成一个长音频
final_audio = concatenate_audioclips(audio_clips).subclip(0, foreground.duration)

# 为合成视频添加背景音乐
final_video = final_video.set_audio(final_audio)

# 导出最终的视频文件
# final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")
# final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, ffmpeg_params=["-hwaccel", "cuda"])
final_video.write_videofile("output_video.mp4", codec="libx264", preset="ultrafast", threads=8)

# final_video.write_videofile("output_video_without_accel.mp4", codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)

