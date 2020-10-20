import sys

from compose.cli.main import main

from dca.arguments import Arguments
from dca.compose import Compose
from dca.config.config import Config
from dca.utils import run_command_in_foreground


class Dispatcher:
    _arguments: Arguments = Arguments()
    _config: Config = None
    _compose: Compose = None

    def run(self):
        argument = self._arguments.parse()
        self._config = Config()
        config = self._config.load()
        self._compose = Compose(config)
        if argument in config['command']:
            self._run_command(argument, config)
        else:
            self._run_compose_command(config)

    def _run_command(self, command: str, config: dict):
        file = self._compose.get()
        if 'container' == config['command'][command]['env']:
            container = config['command'][command]['container']
            content = config['command'][command]['content']
            if isinstance(content, list):
                for c in content:
                    cmd = 'docker exec -i ' + container + ' ' + c
                    run_command_in_foreground(cmd)

    def _run_compose_command(self, config: dict):
        sys.argv.insert(1, '-p')
        sys.argv.insert(2, config['name'])
        sys.argv.insert(3, '-f')
        sys.argv.insert(4, config['compose']['include'])
        main()
