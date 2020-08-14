import argparse


# TODO Refactor this
class Arguments:
    _parser: argparse = None
    config_path: str = None
    start: bool = False
    stop: bool = False

    def __init__(self):
        self._parser = argparse.ArgumentParser(prog = 'dca')
        subparsers = self._parser.add_subparsers(help = 'sub-command help')
        start = subparsers.add_parser('start', help = 'start help', argument_default = False)
        pull = subparsers.add_parser('pull', help = 'pull help', argument_default = False)
        stop = subparsers.add_parser('stop', help = 'stop help', argument_default = False)
        start.set_defaults(start = True, stop = False)
        stop.set_defaults(start = False, stop = True)
        pull.set_defaults(start = False, stop = True)

    def parse(self):
        args = self._parser.parse_args()
        if not args.__dict__:
            self._parser.print_usage()
            exit(0)

        if 'start' in args:
            self.start = args.start
        if 'stop' in args:
            self.stop = args.stop
