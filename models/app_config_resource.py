import os
from typing import Dict, List

from models import ManaConfigResource, SetIconImageConfiguration


class AppConfigResource:
    __mana_config: ManaConfigResource
    __set_icon_image_config: SetIconImageConfiguration
    __resources_dir: str
    __output_dir: str
    __templates_dir: str
    __mana_src: str
    __keyrune_src: str
    __font_dir: str
    __data_dir: str
    __config_file: str
    __generated_images_dir: str
    __tmp_dir: str
    __set_info_template_name: str
    __latex_command: str
    __mysql_user: str
    __mysql_password: str
    __comment_string: str
    __variable_string: str

    @property
    def mana_config(self) -> ManaConfigResource:
        return self.__mana_config

    @property
    def resources_dir(self) -> str:
        return self.__resources_dir

    @property
    def output_dir(self) -> str:
        return self.__output_dir

    @property
    def templates_dir(self) -> str:
        return self.__templates_dir

    @property
    def mana_src(self) -> str:
        return self.__mana_src

    @property
    def keyrune_src(self) -> str:
        return self.__keyrune_src

    @property
    def font_dir(self) -> str:
        return self.__font_dir

    @property
    def data_dir(self) -> str:
        return self.__data_dir

    @property
    def config_file(self) -> str:
        return self.__config_file

    @property
    def generated_images_dir(self) -> str:
        return self.__generated_images_dir

    @property
    def tmp_dir(self) -> str:
        return self.__tmp_dir

    @property
    def set_info_template_name(self) -> str:
        return self.__set_info_template_name

    @property
    def latex_command(self) -> str:
        return self.__latex_command

    @property
    def mysql_user(self) -> str:
        return self.__mysql_user

    @property
    def mysql_password(self) -> str:
        return self.__mysql_password

    @property
    def comment_string(self) -> str:
        return self.__comment_string

    @property
    def variable_string(self) -> str:
        return self.__variable_string

    @property
    def set_icon_image_config(self) -> SetIconImageConfiguration:
        return self.__set_icon_image_config

    @staticmethod
    def create_path(base_dir: str):
        return lambda *args: os.path.join(os.path.dirname(os.path.abspath(base_dir)), *args)

    @staticmethod
    def create_config_from_dict(file_config: Dict, base_dir: str):
        create_path = AppConfigResource.create_path(base_dir)
        resources_dir = create_path(os.environ.get('RESOURCES_DIR', 'resources'))
        output_dir = os.environ.get('OUTPUT_DIR', 'dest')
        templates_dir = create_path(resources_dir, os.environ.get('TEMPLATES_DIR', 'templates'))
        mana_src = create_path(resources_dir, os.environ.get('MANA_ICONS_DIR', 'mana-master/svg'))
        keyrune_src = create_path(resources_dir, os.environ.get('KEYRUNE_ICONS_DIR', 'keyrune-master/svg'))
        font_dir = create_path(resources_dir, os.environ.get('FONT_DIR', 'fonts'))
        data_dir = create_path(resources_dir, os.environ.get('DATA_DIR', 'data'))
        config_file = data_dir + '/' + os.environ.get('CONFIG_FILE', 'config.json')
        generated_images_dir = create_path(resources_dir, os.environ.get('GENERATED_IMAGES_DIR', 'images'))
        tmp_dir = create_path(resources_dir, os.environ.get('TMP', 'tmp'))
        set_info_template_name = os.environ.get('SET_INFO_TEMPLATE_NAME', 'set_info.tex.j2')
        latex_command = os.environ.get('LATEX_COMMAND', 'lualatex')
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_password = os.environ.get('MYSQL_PASSWORD')
        comment_string = os.environ.get('COMMENT_STRING', '@@')
        variable_string = os.environ.get('VARIABLE_STRING', '^^')

        # set image configuration
        text_color = os.environ.get('TEXT_COLOR', '')
        title_stroke_color = os.environ.get('TITLE_STROKE_COLOR', '')
        title_fill_color = os.environ.get('TITLE_FILL_COLOR', '')
        icon_color = os.environ.get('ICON_COLOR', '')

        if mysql_user is None or mysql_password is None:
            raise ValueError('mysql user and password are required')

        if not os.path.exists(data_dir):
            raise ValueError('data directory must exist and not be empty')

        if not os.path.exists(config_file):
            raise ValueError('config file must exist')

        if not os.path.splitext(config_file)[1] == '.json':
            raise ValueError('config file must be in json')

        required_dirs = [output_dir, tmp_dir, resources_dir, templates_dir, mana_src, keyrune_src, font_dir,
                         generated_images_dir, tmp_dir]

        for required_dir in required_dirs:
            if not os.path.exists(required_dir):
                os.makedirs(required_dir)

        env_config = {
            'resources_dir': resources_dir,
            'output_dir': output_dir,
            'templates_dir': templates_dir,
            'mana_src': mana_src,
            'keyrune_src': keyrune_src,
            'font_dir': font_dir,
            'data_dir': data_dir,
            'config_file': config_file,
            'generated_images_dir': generated_images_dir,
            'tmp_dir': tmp_dir,
            'set_info_template_name': set_info_template_name,
            'latex_command': latex_command,
            'mysql_user': mysql_user,
            'mysql_password': mysql_password,
            'comment_string': comment_string,
            'variable_string': variable_string
        }

        set_icon_image_config = dict(**file_config.get('set_icon_image_config', {}), text_color=text_color,
                                     title_stroke_color=title_stroke_color, title_fill_color=title_fill_color,
                                     icon_color=icon_color)

        result = dict(**file_config, **env_config, set_icon_image_config=set_icon_image_config)

        return AppConfigResource(result)

    def __init__(self, config_data: dict[str, str | List[str] | dict]):
        self.__mana_config = ManaConfigResource(config_data.get('mana'))
        self.__resources_dir = config_data.get('resource_dir')
        self.__output_dir = config_data.get('output_dir')
        self.__templates_dir = config_data.get('templates_dir')
        self.__mana_src = config_data.get('mana_src')
        self.__keyrune_src = config_data.get('keyrune_src')
        self.__font_dir = config_data.get('font_dir')
        self.__data_dir = config_data.get('data_dir')
        self.__config_file = config_data.get('config_file')
        self.__generated_images_dir = config_data.get('generated_images_dir')
        self.__tmp_dir = config_data.get('tmp_dir')
        self.__variable_string = config_data.get('variable_string')
        self.__comment_string = config_data.get('comment_string')
        self.__latex_command = config_data.get('latex_command')
        self.__mysql_user = config_data.get('mysql_user')
        self.__mysql_password = config_data.get('mysql_password')
        self.__set_info_template_name = config_data.get('set_info_template_name')
        self.__set_icon_image_config = SetIconImageConfiguration(config_data.get('set_icon_image_config'))
