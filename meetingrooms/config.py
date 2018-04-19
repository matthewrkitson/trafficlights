import json
import pathlib

def get_config_path():
    directory = pathlib.Path(__file__).resolve().parent
    config_file_path = directory.joinpath('meetingrooms.config')
    return str(config_file_path)

def get_config():
    config_path = get_config_path()
    with open(config_path) as json_file:
        config = json.load(json_file)

    return config


