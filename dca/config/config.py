import os

import yamale
import yaml

from dca.arguments import Arguments
from dca.exceptions import YAMLException, ConfigException


class Config:
    __arguments: Arguments = None
    __constants: dict = {}
    __config_path: str = '.dca.yaml'
    project_path: str = None
    config_name: str = None
    config_path: str = None
    project_name: str = None

    def __init__(self, arguments: Arguments):
        self.__arguments = arguments

    def load(self) -> dict:
        if self.__arguments.config_path:
            self.__config_path = self.__arguments.config_path

        absolute_config_path = self.__get_config_absolute_path(self.__config_path)
        if not absolute_config_path:
            raise ConfigException('Cannot find config')
        config = self.__load(absolute_config_path)
        self.__validate(config, absolute_config_path)
        return config

    def __get_config_absolute_path(self, config_path: str, path: str = None) -> str:
        if path is None:
            path = os.getcwd()
        if '/' == path:
            return ''
        search_path = '{0}/{1}'.format(
            path,
            config_path
        )

        if os.path.isfile(search_path):
            self.project_path = path
            return search_path
        return self.__get_config_absolute_path(config_path, os.path.dirname(path))

    def __replace_constants_in_config(self, config):
        if isinstance(config, str):
            return self.__replace_constants(config)
        if isinstance(config, list):
            for i in range(0, len(config)):
                config[i] = self.__replace_constants_in_config(config[i])
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self.__replace_constants_in_config(value)
        return config

    def __replace_constants(self, string: str) -> str:
        for key, value in self.__constants.items():
            string = string.replace('{{' + key + '}}', value)
        return string

    def __validate(self, config: dict, config_path: str) -> dict:
        if 'version' not in config:
            raise ConfigException('no version field in config')
        schema_path = '{schemas_path}/config_schema_v{version}.yaml'.format(
            schemas_path = os.path.dirname(os.path.realpath(__file__)),
            version = config['version']
        )
        if not os.path.isfile(schema_path):
            raise ConfigException('unknown config version ' + str(config['version']))
        schema = yamale.make_schema(schema_path, parser = 'pyyaml')
        data = yamale.make_data(config_path, parser = 'pyyaml')
        yamale.validate(schema, data)
        return config

    def __load(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                file = yaml.load(f)
            return file
        except Exception:
            raise YAMLException('error occurred while loading config file')
