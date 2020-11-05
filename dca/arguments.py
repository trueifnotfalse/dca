import sys
from typing import Optional


class Arguments:
    command: str = None

    def parse(self) -> Optional[str]:
        argv = sys.argv.copy()
        if 2 > len(argv):
            return None
        del argv[0]
        return ' '.join(argv)
