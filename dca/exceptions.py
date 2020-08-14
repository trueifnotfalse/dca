class BaseException(Exception):
    """Base Exception.

    Attributes:
        message -- explanation of the error
    """

class DispatcherException(BaseException):
    """Exception raised for errors in running Dispatcher.
    """


class CommandException(BaseException):
    """Exception raised for errors in running commands.
    """


class ConfigException(BaseException):
    """Exception raised for errors in the Config.
    """

class HostnameException(BaseException):
    """Exception raised for errors in the Container.
    """

class YAMLException(BaseException):
    """Exception raised for errors in save/load YAML files.
    """


class FileException(BaseException):
    """Exception raised for errors in read/write files.
    """
