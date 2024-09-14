from manim import *
from moviepy.editor import VideoFileClip

class VideoBackground(Scene):
    def construct(self):
        # 使用 moviepy 加载视频
        video_path = "radar_data/vecteezy_abstract-plexus-tech-background-with-glowing-blue-shiny_21050150~1.mp4"
        video = VideoFileClip(video_path)

        # 将视频的每一帧转换为 ImageMobject
        video_mobject = ImageMobject(video)

        # 缩放视频大小以适应屏幕
        video_mobject.scale_to_fit_height(config.frame_height)

        # 将视频添加到场景
        self.add(video_mobject)

        # 其他动画效果
        text = Text("这是一个示例文本").set_color(WHITE)
        self.play(Write(text))

        # 保持场景并循环播放视频
        self.wait(10)  # 视频会在10秒内循环播放
