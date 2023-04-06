#!/usr/bin/env python3
import os
import shutil
import sys

from wand.color import Color

import build_icons
from mtg_sql_resource.mtg_sql_resource import MTGSQLResource

if __name__ == "__main__":
    dest = 'dest'
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)
    resource = MTGSQLResource.instantiate('root', 'pass')
    text_color = Color('#2F1F02')
    title_stroke_color = Color('#1F1300')
    icon_color = Color('#C59225')
    svg_folder = '/home/gregorysmith/mtg-list-gen/icons/keyrune-master/svg/'

    for set_name in sys.argv[1:]:
        current_set = resource.get_set(set_name.upper())
        build_icons.process_image(svg_folder + current_set.keyrune_code.lower() + '.svg', current_set.name, dest, 'svg', 'png',
                                  set_image_color=icon_color, text_target_color=text_color,
                                  title_stroke_color=title_stroke_color,text_margin=200)
