import math

from wand.drawing import Drawing
from wand.image import Image, Color
import os

ISO_216_ASPECT_RATIO = math.sqrt(2)


class ImageBuilder:
    src_dir: str
    resource_dir: str
    icon_size: int
    keyrune_dir: str
    mana_dir: str
    font_dir: str

    __color_dict = {
        'b': 'rgb(21,11,0)',
        'c': 'rgb(201,192,190)',
        'g': 'rgb(0,115,62)',
        'r': 'rgb(211,32,42)',
        'u': 'rgb(14,104,171)',
        'w': 'rgb(249,250,244)',
    }

    @staticmethod
    def __convert_to_px(pt, resolution):
        return (pt / 72) * resolution

    @staticmethod
    def __find_file(target_dir: str, target_file_name: str):
        for file in os.listdir(target_dir):
            if os.path.splitext(os.path.basename(file))[0] == os.path.splitext(target_file_name)[0]:
                return os.path.join(target_dir, file)

        raise ValueError('No files named {0} found'.format(target_file_name))

    def __find_keyrune_file(self, target_file: str):
        return ImageBuilder.__find_file(self.keyrune_dir, target_file)

    def __find_mana_icon_file(self, target_mana: str):
        return ImageBuilder.__find_file(self.mana_dir, target_mana)

    def __find_image_file(self, target_file: str):
        return ImageBuilder.__find_file(self.images_dir, target_file)

    def __init__(self, resource_dir, mana_dir, keyrune_dir, images_dir, font_dir, icon_size=64, resolution=4096):
        self.resource_dir = resource_dir
        self.icon_size = icon_size
        self.resolution = resolution
        self.mana_dir = mana_dir
        self.keyrune_dir = keyrune_dir
        self.images_dir = images_dir
        self.font_dir = font_dir

    def create_mana_icon(self, color: str, background='transparent', source_alpha_color='#666666', target_type='png'):
        filepath = self.__find_mana_icon_file(color.lower())
        target_path = os.path.join(self.images_dir, color.lower() + '.' + target_type)
        color_val = Color(self.__color_dict.get(color))
        with Image(filename=filepath, resolution=self.resolution, background=Color(background)) as image:
            image.colorize(color_val, Color(source_alpha_color))
            image.antialias = True
            image.resize(self.icon_size, self.icon_size)
            image.save(filename=target_path)

    def create_multi_color_mana_icons(self, target_name: str, colors: [str], target_type='png'):
        target_path = os.path.join(self.images_dir, target_name + '.' + target_type)
        with Image(height=self.icon_size, width=self.icon_size + int(self.icon_size * (len(colors) / 2))) as image:
            for i, color in enumerate(colors):
                target_file_path = self.__find_image_file(color)
                with Image(filename=target_file_path) as icon:
                    image.composite(icon, left=int(i * (self.icon_size / 2)), top=0)
            image.save(filename=target_path)

    def create_set_image(self, set_code: str, set_name: str, background='transparent', target_image_size=1024,
                         set_font='beleren-bold_P1.01.ttf',
                         source_alpha_color='#666666', set_image_color='black',
                         text_target_color='#666666', title_stroke_color='#666666', text_margin=200, target_type='png'):
        target_file = self.__find_keyrune_file(set_code)
        target_path = os.path.join(self.images_dir, set_code + '.' + target_type)

        with Image(filename=target_file, resolution=self.resolution, background=Color(background)) as image:
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
                    text_width_px = ImageBuilder.__convert_to_px(metrics.text_width, self.resolution)
                    if text_width_px < canvas_width - text_margin:
                        draw.font_size += 0.1
                    else:
                        final_text_height = ImageBuilder.__convert_to_px(metrics.text_height, self.resolution)
                        title_font_size = draw.font_size
                        break
                text_height_to_image_height = final_text_height / image.height
                if set_name.find(':') > 0:
                    main_title, subtitle = set_name.upper().split(': ')
                    draw.font_size = title_font_size * 0.5
                    subtitle_height = ImageBuilder.__convert_to_px(draw.get_font_metrics(image, subtitle).text_height,
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
