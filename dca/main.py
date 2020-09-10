import sys

from dca.dispatcher import Dispatcher


def main():
    try:
        command = Dispatcher()
        command.run()
    except (KeyboardInterrupt):
        exit(1)
