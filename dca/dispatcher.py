import functools
import sys

import yaml
from compose.cli.docopt_command import DocoptDispatcher
from compose.cli.main import TopLevelCommand, setup_console_handler, console_handler, set_no_color_if_clicolor, setup_parallel_logger, perform_command

from dca.arguments import Arguments
from dca.config.config import Config


class Dispatcher:
    _arguments: Arguments = Arguments()
    _config: Config = None

    def run(self):
        self._arguments.parse()
        self._config = Config(self._arguments)
        config = self._config.load()
        self.__command_line_mode(config)

    def __command_line_mode(self, config):
        path = config['compose']['include']
        with open(path, 'r') as f:
            file = yaml.load(f)

        #print(file)
        dispatcher = DocoptDispatcher(
            TopLevelCommand,
            {'options_first': True})

        options, handler, command_options = dispatcher.parse(sys.argv[1:])
        options['COMMAND'] = 'pull'
        #options['ARGS']= ['-d']
        options['--file'] = ['develop/docker-compose.yml']
        setup_console_handler(console_handler,
                              options.get('--verbose'),
                              set_no_color_if_clicolor(options.get('--no-ansi')),
                              options.get("--log-level"))
        setup_parallel_logger(set_no_color_if_clicolor(options.get('--no-ansi')))
        print(command_options)
        print(options)
        c = functools.partial(perform_command, options, handler, command_options)
        c()

