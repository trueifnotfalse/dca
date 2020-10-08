import functools
import sys

import yaml
from compose.cli.docopt_command import DocoptDispatcher
from compose.cli.main import TopLevelCommand, setup_console_handler, console_handler, set_no_color_if_clicolor, setup_parallel_logger, perform_command

from dca.arguments import Arguments
from dca.config.config import Config
from compose.cli.main import main
from dca.utils import run_command_in_foreground


class Dispatcher:
    _arguments: Arguments = Arguments()
    _config: Config = None

    def run(self):
        argument = self._arguments.parse()
        self._config = Config()
        config = self._config.load()
        if argument in config['command']:
            self._run_command(argument, config)
        else:
            self._run_compose_command(config)

    def _run_command(self, command: str, config: dict):
        path =config['compose']['include']
        with open(path, 'r') as f:
            file = yaml.load(f)
        if 'container' == config['command'][command]['env']:
            container = config['command'][command]['container']
            cn = file['services'][container]['container_name']
            content = config['command'][command]['content']
            if isinstance(content, list):
                for c in content:
                    cmd = 'docker exec -i '+cn+' '+c
                    run_command_in_foreground(cmd)


    def _run_compose_command(self, config: dict):
        sys.argv.insert(1, '-p')
        sys.argv.insert(2, config['name'])
        sys.argv.insert(3, '-f')
        sys.argv.insert(4, config['compose']['include'])
        main()
