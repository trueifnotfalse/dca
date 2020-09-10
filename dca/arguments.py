import sys


class Arguments:
    command: str = None

    def parse(self):
        argv = sys.argv
        if 2 > len(argv):
            return
        self.command = argv[1]
