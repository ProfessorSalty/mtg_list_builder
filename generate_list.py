#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import shutil
import sys

from wand.color import Color
import pandas as pd

from jinja2 import Environment, FileSystemLoader

import build_icons
from mtg_sql_resource.mtg_sql_resource import MTGSQLResource

load_dotenv()

if __name__ == "__main__":
    output_dir = os.environ.get('OUTPUT_DIR')
    templates_dir = os.environ.get('TEMPLATES_DIR')
    mana_src = os.environ.get('MANA_ICONS_DIR')
    keyrune_src = os.environ.get('KEYRUNE_ICONS_DIR')
    generated_images_dir = os.environ.get('GENERATED_IMAGES_DIR')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_password = os.environ.get('MYSQL_PASSWORD')

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    colors = ['b', 'c', 'g', 'r', 'u', 'w']

    for color in colors:
        build_icons.create_color_icon(color, mana_src, output_dir, 'svg', 'png')

    combos = [
        ('B', 'Black'),
        ('U', 'Blue'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('W', 'White'),
        ('B,G', 'Golgari'),
        ('R,U', 'Izzet'),
        ('B,R', 'Rekdos'),
        ('B,U', 'Dimir'),
        ('B,W', 'Orzhsov'),
        ('G,R', 'Gruul'),
        ('G,U', 'Simic'),
        ('G,W', 'Selesnya'),
        ('R,W', 'Boros'),
        ('U,W', 'Zorius'),
        ('B,G,W', 'Abzan'),
        ('G,U,W', 'Bant'),
        ('B,U,W', 'Esper'),
        ('B,R,U', 'Grixis'),
        ('R,U,W', 'Jeskai'),
        ('B,G,R', 'Jund'),
        ('B,R,W', 'Mardu'),
        ('G,R,W', 'Naya'),
        ('B,G,U', 'Sultai'),
        ('G,R,U', 'Temur'),
        ('B,G,R,U', 'Glint'),
        ('B,G,W,R', 'Dune'),
        ('G,U,W,R', 'Ink'),
        ('B,R,U,W', 'Yore'),
        ('B,G,U,W', 'Witch'),
    ]

    for (colors, name) in combos:
        build_icons.create_multi_color_icons(name, colors.split(','), output_dir, output_dir, 'png', 'png')

    resource = MTGSQLResource.instantiate(mysql_user, mysql_password)
    text_color = Color('#543800')
    title_stroke_color = Color('#1F1300')
    icon_color = Color('#E6F7FF')
    env = Environment(loader=FileSystemLoader(templates_dir))

    for requested_set_code in sys.argv[1:]:
        current_set = resource.get_set(requested_set_code.upper())
        if current_set is None:
            continue
        build_icons.create_set_image(keyrune_src + current_set.keyrune_code.lower() + '.svg', current_set.name, output_dir,
                                  'svg',
                                  'png',
                                     set_image_color=icon_color, text_target_color=text_color,
                                     title_stroke_color=title_stroke_color, text_margin=200)

        df = pd.DataFrame(current_set.cards)
        rarity_totals = df.groupby("rarity").size().reset_index(name="count")
        all_color_totals = df.groupby("color_name").size().reset_index(name="count")
        color_totals = all_color_totals[all_color_totals['color_name'].isin(colors)]
        multi_color_totals = all_color_totals[~all_color_totals['color_name'].isin(colors)]
        release_date = current_set.release_date
        set_code = current_set.code

        template = env.get_template('template_name.html')
        rendered_template = template.render(set_code=set_code, release_date=release_date,
                                            card_total=len(current_set.cards), color_totals=color_totals,
                                            multi_color_totals=multi_color_totals)
