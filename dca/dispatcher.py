import sys
from typing import Dict

from compose.cli.main import main

from dca.arguments import Arguments
from dca.command import Command
from dca.compose import Compose
from dca.config.config import Config


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
        if argument in self._command_list:
            self._run_command(argument)
        else:
            self._run_compose_command(config)

    def _run_command(self, command: str):
        if self._command_list[command].is_self():
            for c in self._command_list[command].content:
                self._run_command(c)
        else:
            self._command_list[command].run()

    def _run_compose_command(self, config: dict):
        sys.argv.insert(1, '-p')
        sys.argv.insert(2, config['name'])
        sys.argv.insert(3, '-f')
        sys.argv.insert(4, config['compose']['include'])
        main()

    def _create_command_list(self, config: dict) -> dict:
        command_list = {}
        for command in config['command']:
            command_list[command] = Command(config['command'][command])
        return command_list
