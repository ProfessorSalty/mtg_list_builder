#!/usr/bin/env python3

import os
import subprocess
from dotenv import load_dotenv
import sys
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from image_resource import ImageBuilder
from models import AppConfigResource
from mtg_sql_resource import MTGSQLResource

load_dotenv()

if __name__ == "__main__":
    execution_path, *set_rarities = sys.argv

    create_path = AppConfigResource.create_path(execution_path)
    resources_dir = create_path(os.environ.get('RESOURCES_DIR', 'resources'))
    data_dir = create_path(resources_dir, os.environ.get('DATA_DIR', 'data'))
    config_file = data_dir + '/' + os.environ.get('CONFIG_FILE', 'config.json')

    with open(config_file, 'r') as config_file_read:
        app_config_resource = AppConfigResource.create_config_from_dict(json.load(config_file_read), execution_path)

    image_resource = ImageBuilder(resource_dir=resources_dir, mana_dir=app_config_resource.mana_src,
                                  keyrune_dir=app_config_resource.keyrune_src,
                                  images_dir=app_config_resource.generated_images_dir,
                                  font_dir=app_config_resource.font_dir)

    for color in app_config_resource.mana_config.base_colors:
        image_resource.create_mana_icon(color)

    for combo in app_config_resource.mana_config.combos:
        name = combo.get('name')
        colors = combo.get('colors')
        image_resource.create_multi_color_mana_icons(name, colors.lower().split(','))

    db = MTGSQLResource.instantiate(app_config_resource.mysql_user, app_config_resource.mysql_password)
    env = Environment(loader=FileSystemLoader(app_config_resource.templates_dir),
                      comment_start_string=app_config_resource.comment_string,
                      comment_end_string=app_config_resource.comment_string,
                      variable_start_string=app_config_resource.variable_string,
                      variable_end_string=app_config_resource.variable_string)

    for requested_set_code in set_rarities:
        set_code, rarities = requested_set_code.split(':')
        current_set = db.get_set(set_code)
        if current_set is None:
            continue

        image_resource.create_set_image(current_set.keyrune_code.lower(), name,
                                        set_image_color=app_config_resource.set_icon_image_config.icon_color,
                                        text_target_color=app_config_resource.set_icon_image_config.text_color,
                                        title_stroke_color=app_config_resource.set_icon_image_config.title_stroke_color)

        cards_dataframe = pd.DataFrame(current_set.cards)
        rarity_totals = cards_dataframe.groupby("rarity").size().reset_index(name="count").values
        all_color_totals = cards_dataframe.groupby("color_name").size().reset_index(name="count")
        color_totals = all_color_totals[
            all_color_totals['color_name'].isin(app_config_resource.mana_config.base_color_names)].values
        multi_color_totals = all_color_totals[
            ~all_color_totals['color_name'].isin(app_config_resource.mana_config.base_color_names)].values

        template = env.get_template(app_config_resource.set_info_template_name)
        rendered_template = template.render(set_code=set_code, release_date=current_set.release_date,
                                            cards_total=len(current_set.cards), color_totals=color_totals,
                                            multi_color_totals=multi_color_totals, rarity_totals=rarity_totals,
                                            image_dir=app_config_resource.generated_images_dir,
                                            font_dir=app_config_resource.font_dir)
        output_filename = f'{set_code}_set_info'
        tex_output = os.path.join(app_config_resource.tmp_dir, f'{output_filename}.tex')
        with open(tex_output, 'w') as temp_file:
            temp_file.write(rendered_template)

        process = subprocess.Popen([app_config_resource.latex_command, tex_output], stdout=subprocess.PIPE)

        output, error = process.communicate()

        if process.returncode != 0:
            sys.exit(process.returncode)

        pdf_filename = os.path.join(app_config_resource.output_dir, f'{output_filename}.pdf')
        subprocess.run(['mv', f'{tex_output[:-3]}.pdf', pdf_filename])
