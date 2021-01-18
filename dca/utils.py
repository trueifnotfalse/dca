import os

import yaml

from dca.exceptions import CommandException, YAMLException


def load_yaml(path):
    try:
        with open(path, 'r') as f:
            file = yaml.load(f)
        return file
    except Exception:
        raise YAMLException('error occurred while loading yaml file')


def save_yaml(path, data):
    try:
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style = False, allow_unicode = True)
    except Exception:
        raise YAMLException('error occurred while saving yaml file')


def dict_merge(dst, src):
    for k, v in src.items():
        if k in dst and isinstance(dst[k], dict):
            dict_merge(dst[k], src[k])
        else:
            dst[k] = src[k]


def insert_str(string: str, str_to_insert: str, index: int) -> str:
    return string[:index] + str_to_insert + string[index:]


def run_command_in_foreground(command, output = True) -> int:
    if output:
        print('running command: ' + command)
    try:
        exit_code = os.system(command)
        return int(exit_code)
    except Exception as e:
        raise CommandException('error occurred when executing command in foreground ' + str(e))
