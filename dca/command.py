from typing import Union

from dca.utils import run_command_in_foreground


class Command:
    name: str = None
    env: str = None
    container: str = None
    interpreter: str = None
    content: Union[str, list]

    def run(self):
        if 'container' == self.env:
            if isinstance(self.content, list):
                for c in self.content:
                    cmd = 'docker exec -i ' + self.container + ' ' + c
                    run_command_in_foreground(cmd)
