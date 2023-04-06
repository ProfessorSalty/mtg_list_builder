#!/usr/bin/env python3
from wand.image import Image, Color
from wand.drawing import Drawing
import os
from pathlib import Path
import shutil


def build_icons(target_dir: str, dest: str, source_type: str, target_type='png'):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)

    t = Path(target_dir)
    for file in t.glob(f'*.{source_type}'):
        process_image(file, dest, source_type, target_type)


def process_image(filename: str, printed_name: str, dest: str, source_type: str, target_type: str, resolution=4096,
                  background=Color('transparent'), target_size=1024, font_path='./fonts/beleren-bold_P1.01.ttf',
                  source_alpha_color=Color('#666666'), set_image_color=Color('black'),
                  text_target_color=Color('#666666'), title_stroke_color=Color('#666666'), text_margin=20):
    image_name = os.path.basename(filename).replace(f'.{source_type}', f'.{target_type}')
    target_path = os.path.join(dest, image_name)
    with Image(filename=filename, resolution=resolution, background=background) as image:
        canvas_width = target_size * 2
        image.colorize(set_image_color, source_alpha_color)
        image.resize(target_size, target_size)
        image.extent(width=canvas_width, height=target_size, gravity='south')
        image.antialias = True
        title = printed_name.replace(': ', '\n').upper()
        with Drawing() as draw:
            draw.font = font_path
            draw.fill_color = text_target_color
            draw.font_size = 1
            draw.gravity = 'south'
            while True:
                metrics = draw.get_font_metrics(image, title, multiline=True)
                text_width_px = convert_to_px(metrics.text_width, resolution)
                if text_width_px < canvas_width - text_margin:
                    draw.font_size += 0.1
                else:
                    final_text_height = convert_to_px(metrics.text_height, resolution)
                    title_font_size = draw.font_size
                    break
            text_height_to_image_height = final_text_height / image.height
            if printed_name.find(':') > 0:
                main_title, subtitle = printed_name.upper().split(': ')
                draw.font_size = title_font_size * 0.5
                subtitle_height = convert_to_px(draw.get_font_metrics(image, subtitle).text_height, resolution)
                draw.text(0, 0, subtitle)
                draw.font_size = title_font_size * 1.4
                draw.stroke_color = title_stroke_color
                draw.stroke_width = 10
                draw.text(0, int(subtitle_height + text_height_to_image_height), main_title)
                draw(image)
            else:
                draw.stroke_color = title_stroke_color
                draw.stroke_width = 10
                draw.text(0, int(text_height_to_image_height), title)
                draw(image)
        image.save(filename=target_path)


def convert_to_px(pt, resolution):
    return (pt / 72) * resolution


if __name__ == "__main__":
    text_color = Color('#2F1F02')
    title_stroke_color = Color('#1F1300')
    icon_color = Color('#C59225')
    process_image('/home/gregorysmith/mtg-list-gen/icons/keyrune-master/svg/3ed.svg', 'Revised', '.',
                  'svg', 'png', set_image_color=icon_color, text_target_color=text_color,
                  title_stroke_color=title_stroke_color, text_margin=300)
    process_image('/home/gregorysmith/mtg-list-gen/icons/keyrune-master/svg/one.svg', 'Phyrexia: All Will Be One', '.',
                  'svg', 'png', set_image_color=icon_color, text_target_color=text_color,
                  title_stroke_color=title_stroke_color, text_margin=300)
