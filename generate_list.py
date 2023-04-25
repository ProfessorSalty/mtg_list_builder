#!/usr/bin/env python3
import os
import subprocess

from dotenv import load_dotenv
import shutil
import sys

import pandas as pd

from jinja2 import Environment, FileSystemLoader

from image_resource import ImageBuilder
from mtg_sql_resource import MTGSQLResource

load_dotenv()

base_color_names = ['Black', 'Blue', 'Green', 'Red', 'White']
base_colors = ['b', 'c', 'g', 'r', 'u', 'w']
comment_string = '@@'
variable_string = '^^'

if __name__ == "__main__":
    def create_path(*args):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)


    resources_dir = create_path(os.environ.get('RESOURCES_DIR', 'resources'))
    output_dir = os.environ.get('OUTPUT_DIR', 'dest')
    templates_dir = create_path(resources_dir, os.environ.get('TEMPLATES_DIR', 'templates'))
    mana_src = create_path(resources_dir, os.environ.get('MANA_ICONS_DIR', 'mana-master/svg'))
    keyrune_src = create_path(resources_dir, os.environ.get('KEYRUNE_ICONS_DIR', 'keyrune-master/svg'))
    font_dir = create_path(resources_dir, os.environ.get('FONT_DIR', 'fonts'))
    generated_images_dir = create_path(resources_dir, os.environ.get('GENERATED_IMAGES_DIR', 'images'))
    tmp_dir = create_path(resources_dir, os.environ.get('TMP', 'tmp'))
    set_info_template_name = os.environ.get('SET_INFO_TEMPLATE_NAME', 'set_info.tex.j2')
    latex_command = os.environ.get('LATEX_COMMAND', 'lualatex')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_password = os.environ.get('MYSQL_PASSWORD')

    if mysql_user is None or mysql_password is None:
        raise ValueError('mysql user and password are required')

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    required_dirs = [output_dir, tmp_dir, resources_dir, templates_dir, mana_src, keyrune_src, font_dir, generated_images_dir, tmp_dir, set_info_template_name]
    for dir in required_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


    image_resource = ImageBuilder(resource_dir=resources_dir, mana_dir=mana_src, keyrune_dir=keyrune_src,
                                  images_dir=generated_images_dir, font_dir=font_dir)

    for color in base_colors:
        image_resource.create_mana_icon(color)

    combos = [
        ('b', 'Black'),
        ('u', 'Blue'),
        ('r', 'Red'),
        ('g', 'Green'),
        ('w', 'White'),
        ('b,g', 'Golgari'),
        ('r,u', 'Izzet'),
        ('b,r', 'Rekdos'),
        ('b,u', 'Dimir'),
        ('b,w', 'Orzhsov'),
        ('g,r', 'Gruul'),
        ('g,u', 'Simic'),
        ('g,w', 'Selesnya'),
        ('r,w', 'Boros'),
        ('u,w', 'Zorius'),
        ('b,g,w', 'Abzan'),
        ('g,u,w', 'Bant'),
        ('b,u,w', 'Esper'),
        ('b,r,u', 'Grixis'),
        ('r,u,w', 'Jeskai'),
        ('b,g,r', 'Jund'),
        ('b,r,w', 'Mardu'),
        ('g,r,w', 'Naya'),
        ('b,g,u', 'Sultai'),
        ('g,r,u', 'Temur'),
        ('b,g,r,u', 'Glint'),
        ('b,g,w,r', 'Dune'),
        ('g,u,w,r', 'Ink'),
        ('b,r,u,w', 'Yore'),
        ('b,g,u,w', 'Witch'),
    ]

    for (combo_colors, name) in combos:
        image_resource.create_multi_color_mana_icons(name, combo_colors.lower().split(','))

    db = MTGSQLResource.instantiate(mysql_user, mysql_password)
    text_color = '#543800'
    title_stroke_color = '#1F1300'
    icon_color = '#E6F7FF'
    env = Environment(loader=FileSystemLoader(templates_dir), comment_start_string=comment_string,
                      comment_end_string=comment_string, variable_start_string=variable_string,
                      variable_end_string=variable_string)

    for requested_set_code in sys.argv[1:]:
        current_set = db.get_set(requested_set_code.upper())
        if current_set is None:
            continue
        image_resource.create_set_image(current_set.keyrune_code.lower(), current_set.name,
                                        set_image_color=icon_color, text_target_color=text_color,
                                        title_stroke_color=title_stroke_color)

        df = pd.DataFrame(current_set.cards)
        rarity_totals = df.groupby("rarity").size().reset_index(name="count").values
        all_color_totals = df.groupby("color_name").size().reset_index(name="count")
        color_totals = all_color_totals[all_color_totals['color_name'].isin(base_color_names)].values
        multi_color_totals = all_color_totals[~all_color_totals['color_name'].isin(base_color_names)].values
        release_date = current_set.release_date
        set_code = current_set.code.lower()

        template = env.get_template(set_info_template_name)
        rendered_template = template.render(set_code=set_code, release_date=release_date,
                                            cards_total=len(current_set.cards), color_totals=color_totals,
                                            multi_color_totals=multi_color_totals, rarity_totals=rarity_totals,
                                            image_dir=generated_images_dir, font_dir=font_dir)
        output_filename = f'{set_code}_set_info'
        tex_output = os.path.join(tmp_dir, f'{output_filename}.tex')
        with open(tex_output, 'w') as temp_file:
            temp_file.write(rendered_template)

        process = subprocess.Popen([latex_command,  tex_output], stdout=subprocess.PIPE)

        output, error = process.communicate()

        if process.returncode != 0:
            sys.exit(process.returncode)

        pdf_filename = os.path.join(output_dir, f'{output_filename}.pdf')
        subprocess.run(['mv', f'{tex_output[:-3]}.pdf', pdf_filename])
