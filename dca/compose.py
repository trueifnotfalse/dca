import yaml


class Compose:
    _config: dict = {}

    def __init__(self, config: dict):
        self._config = config

    def get(self) -> dict:
        if 'compose' not in self._config:
            return {}
        if 'include' not in self._config['compose']:
            return {}
        path = self._config['compose']['include']
        with open(path, 'r') as f:
            file = yaml.load(f)
        return file
