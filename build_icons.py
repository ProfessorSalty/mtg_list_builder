#!/usr/bin/env python3
from wand.image import Image, Color
from wand.drawing import Drawing
import os


class ImageBuilder:
    src_dir: str
    resource_dir: str
    icon_size: int
    output_dir: str

    __color_dict = {
        'b': 'rgb(21,11,0)',
        'c': 'rgb(201,192,190)',
        'g': 'rgb(0,115,62)',
        'r': 'rgb(211,32,42)',
        'u': 'rgb(14,104,171)',
        'w': 'rgb(249,250,244)',
    }

    def __init__(self, src_dir: str, resource_dir: str, icon_size=64, resolution=4096, output_dir='../dest'):
        self.src_dir = src_dir
        self.resource_dir = resource_dir
        self.icon_size = icon_size
        self.resolution = resolution
        self.output_dir = output_dir

    def create_multi_color_icons(self, name: str, colors: [str]):
        target_path = os.path.join(self.output_dir, name.lower())
        with Image(height=self.icon_size, width=self.icon_size + int(self.icon_size * (len(colors) / 2))) as image:
            for i, color in enumerate(colors):
                with Image(filename=os.path.join(self.src_dir, color.lower())) as icon:
                    image.composite(icon, left=int(i * (self.icon_size / 2)), top=0)
            image.save(filename=target_path)

    def create_color_icon(self, color: str, background='transparent', source_alpha_color='#666666'):
        filepath = os.path.join(self.src_dir, color.lower())
        target_path = os.path.join(self.output_dir, color.lower())
        color_val = Color(self.__color_dict.get(color))
        with Image(filename=filepath, resolution=self.resolution, background=Color(background)) as image:
            image.colorize(color_val, Color(source_alpha_color))
            image.antialias = True
            image.resize(self.icon_size, self.icon_size)
            image.save(filename=target_path)

    def create_set_image(self, filename: str, set_name: str, background='transparent', target_image_size=1024,
                         set_font='./fonts/beleren-bold_P1.01.ttf',
                         source_alpha_color='#666666', set_image_color='black',
                         text_target_color='#666666', title_stroke_color='#666666', text_margin=20):
        target_path = os.path.join(self.output_dir, filename)
        with Image(filename=filename, resolution=self.resolution, background=Color(background)) as image:
            canvas_width = target_image_size * 2
            image.alpha_channel = 'flatten'
            image.colorize(Color(set_image_color), Color(source_alpha_color))
            image.resize(target_image_size, target_image_size)
            image.extent(width=canvas_width, height=target_image_size, gravity='south')
            image.antialias = True
            title = set_name.replace(': ', '\n').upper()
            with Drawing() as draw:
                draw.font = set_font
                draw.fill_color = Color(text_target_color)
                draw.font_size = 1
                draw.gravity = 'south'
                while True:
                    metrics = draw.get_font_metrics(image, title, multiline=True)
                    text_width_px = self.convert_to_px(metrics.text_width, self.resolution)
                    if text_width_px < canvas_width - text_margin:
                        draw.font_size += 0.1
                    else:
                        final_text_height = self.convert_to_px(metrics.text_height, self.resolution)
                        title_font_size = draw.font_size
                        break
                text_height_to_image_height = final_text_height / image.height
                if set_name.find(':') > 0:
                    main_title, subtitle = set_name.upper().split(': ')
                    draw.font_size = title_font_size * 0.5
                    subtitle_height = self.convert_to_px(draw.get_font_metrics(image, subtitle).text_height,
                                                         self.resolution)
                    draw.text(0, 0, subtitle)
                    draw.font_size = title_font_size * 1.4
                    draw.stroke_color = Color(title_stroke_color)
                    draw.stroke_width = 10
                    draw.text(0, int(subtitle_height + text_height_to_image_height), main_title)
                    draw(image)
                else:
                    draw.stroke_color = Color(title_stroke_color)
                    draw.stroke_width = 10
                    draw.text(0, int(text_height_to_image_height), title)
                    draw(image)
            image.save(filename=target_path)

    @staticmethod
    def convert_to_px(pt, resolution):
        return (pt / 72) * resolution

# def faster_generate_message(msg):
#     with Image(filename='wizard:') as img:
#         dim = img.size
#         with Image() as txt:
#             # Set typeface properties before reading label:
#             txt.background_color = 'transparent'
#             txt.font_color = 'magenta'
#             txt.font_path = kFontPath
#             # Picking either the min / max will generate a real large image.
#             txt.font_size = min(*dim)
#             txt.read(filename='label:' + msg)
#             # If we want message to hit the border of the image.
#             txt.trim(fuzz=0.1 * txt.quantum_range)
#             # Resize respecting the largest side.
#             txt.transform(resize='{0}x{1}>'.format(*dim))
#             # Compose over the original image.
#             img.composite(txt, gravity='center')
#         # Just to show the image when displayed online.
#         img.border('cyan', 1, 1)
#         img.save(filename='output.png')
