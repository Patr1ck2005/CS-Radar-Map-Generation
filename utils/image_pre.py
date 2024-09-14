import os
from pathlib import Path

from PIL import Image, ImageDraw
from manim import ImageMobject


def crop_image_to_circle(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")  # 打开图片并转换为RGBA模式（支持透明）

    # 创建一个与图像同样大小的透明背景
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    # 在遮罩上绘制一个白色的圆形
    draw.ellipse((0, 0) + img.size, fill=255)

    # 将圆形应用为遮罩，保留圆形内的内容，外部设为透明
    img.putalpha(mask)

    # 保存裁剪后的图片
    img.save(output_path, format="PNG")


def manim_crop_image_to_circle(image_path):
    # 创建一个临时文件来存储裁剪后的图片
    image_dir = os.path.dirname(image_path)
    image_name = Path(image_path).stem  # 直接获取不带扩展名的文件名
    temp_dir = os.path.join(image_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_image_path = os.path.join(temp_dir, f"{image_name}_cropped_image.png")

    # 打开图像并转换为RGBA模式以支持透明
    img = Image.open(image_path).convert("RGBA")

    # 创建一个圆形遮罩
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)  # 在遮罩上绘制一个白色圆形

    # 将遮罩应用到图片，使圆形以外的部分变为透明
    img.putalpha(mask)

    # 将裁剪后的图像保存为临时文件
    img.save(temp_image_path, format="PNG")

    # 返回裁剪后的ImageMobject
    return ImageMobject(temp_image_path)


def manim_apply_opacity_to_image(image_path, opacity):
    # 获取输入图像的目录和文件名
    image_dir = os.path.dirname(image_path)
    image_name = Path(image_path).stem  # 获取文件名（无扩展名）
    temp_dir = os.path.join(image_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)  # 如果 temp 文件夹不存在则创建
    temp_image_path = os.path.join(temp_dir, f"{image_name}_with_opacity.png")

    # 打开图像并转换为 RGBA 模式以支持透明度
    img = Image.open(image_path).convert("RGBA")

    # 提取 alpha 通道（透明度通道）
    alpha = img.split()[3]  # 获取 alpha 通道
    # 调整透明度，保持原有透明区域，并整体应用输入的透明度
    alpha = alpha.point(lambda p: p * opacity)  # 乘以透明度系数
    img.putalpha(alpha)  # 将修改后的透明度应用到图像

    # 保存修改后的图像到临时文件
    img.save(temp_image_path, format="PNG")

    # 返回处理后的 ImageMobject
    return ImageMobject(temp_image_path)
