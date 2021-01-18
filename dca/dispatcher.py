import os
import sys
from typing import Dict

from compose.cli.main import main

from dca.arguments import Arguments
from dca.command import Command
from dca.compose import Compose
from dca.config.config import Config
from dca.exceptions import FileException


class Dispatcher:
    _arguments: Arguments = Arguments()
    _config: Config = None
    _compose: Compose = None
    _command_list: Dict[str, Command] = {}

    def run(self):
        argument = self._arguments.parse()
        self._config = Config()
        config = self._config.load()
        self._command_list = self._create_command_list(config)
        self._run_command(argument, config)

    def _run_command(self, command: str, config: dict):
        if command in self._command_list:
            if self._command_list[command].is_self():
                for c in self._command_list[command].content:
                    self._run_command(c, config)
            else:
                self._command_list[command].run()
        else:
            self._run_compose_command(command, config)

    def _run_compose_command(self, command: str, config: dict):
        argv = [
            sys.argv[0],
            '-p',
            config['name'],
            '-f',
            self._get_compose_config_path(config),
        ]

        sys.argv = argv + command.split(' ')
        main()

    def _create_command_list(self, config: dict) -> dict:
        command_list = {}
        for command in config['command']:
            command_list[command] = Command(config['command'][command])
        return command_list

    def _get_compose_config_path(self, config: dict) -> str:
        path = config['compose']['include']
        if os.path.exists(path):
            return path

        path = self._get_project_dir() + path
        if os.path.exists(path):
            return path

        raise FileException('Cannot find compose config file.')

    def _get_project_dir(self) -> str:
        return self._config.project_path + '/'
