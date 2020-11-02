from abc import ABCMeta


class AbstractMagicObject(metaclass = ABCMeta):

    def __init__(self, params: dict):
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
