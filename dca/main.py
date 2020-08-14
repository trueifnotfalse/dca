import sys

from dca.dispatcher import Dispatcher


def main():
    try:
        print(sys.argv)
        exit(0)
        command = Dispatcher()
        command.run()
    except (KeyboardInterrupt):
        exit(1)
