#!/usr/bin/env python3
import datetime
import os
import sys
from typing import Dict

from dotenv import load_dotenv

from mtg_sql_resource import MTGSQLResource
from models import SetRarity

load_dotenv()
set_code_card_list = Dict[str, str | list[str]]


def get_card_info(set_rarity_pair: SetRarity) -> set_code_card_list:
    set_code = set_rarity_pair.set_name
    rarities = set_rarity_pair.rarities
    cards = db.get_cards_by_rarity(set_code, rarities)
    return {
        'set_code': set_code,
        'card_list': cards
    }


if __name__ == "__main__":
    output_dir = os.environ.get('OUTPUT_DIR', 'dest')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_password = os.environ.get('MYSQL_PASSWORD')

    if mysql_user is None or mysql_password is None:
        raise ValueError('mysql user and password are required')

    db = MTGSQLResource.instantiate(mysql_user, mysql_password)

    set_rarity_pairs = SetRarity.create_list_from_input_args(sys.argv)

    formatted_lines = [get_card_info(a) for a in set_rarity_pairs]
    combined_filename = f"{output_dir}/{'-'.join([a.get('set_code') for a in formatted_lines])}-{datetime.datetime.now()}.txt"

    with open(combined_filename, 'w') as combined_file:
        combined_file.write('#### SUMMARY ####\n\n')

        for line in formatted_lines:
            combined_file.write(f"{line.get('set_code')}: {len(line.get('card_list'))}\n")

        combined_file.write('\n#### CARDS ####\n\n')

        total = sum(len(line.get('card_list')) for line in formatted_lines)
        combined_file.write(f"Total: {total}")
        combined_file.write("\n\n")

        for line in formatted_lines:
            for card in line.get('card_list'):
                combined_file.write(f"{card} [{line.get('set_code')}]\n")
            combined_file.write("\n")



