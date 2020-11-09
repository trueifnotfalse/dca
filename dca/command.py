from typing import Union

from dca.abstract.abstract_magic_object import AbstractMagicObject
from dca.utils import run_command_in_foreground


class Command(AbstractMagicObject):
    name: str = None
    env: str = None
    container: str = None
    interpreter: str = None
    content: Union[str, list] = None

    def run(self):
        if self.is_container():
            if isinstance(self.content, list):
                for c in self.content:
                    cmd = 'docker exec -it ' + self.container + ' ' + c
                    run_command_in_foreground(cmd)

    def is_self(self):
        return 'self' == self.env

    def is_container(self):
        return 'container' == self.env

    def is_local(self):
        return 'local' == self.env
