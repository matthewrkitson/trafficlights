import json
import os
import stat
import pathlib

def get_config_path(name):
    directory = pathlib.Path(__file__).resolve().parent
    config_file_path = directory.joinpath(name + '.config')
    return str(config_file_path)

def get_config(name, sensitive=False):
    config_path = get_config_path(name)
    if sensitive:
        mode = os.stat(config_path)[stat.ST_MODE]
        print("Mode is " + oct(mode))
        if mode & 0o0777 != 0o0400:
            raise PermissionError("The confg file " + config_path + " contains sensitive information. \n" 
                "It's permission mask must be 0400 to prevent anyone else reading it.")
    try:
        with open(config_path) as json_file:
            config = json.load(json_file)
    except Exception as ex:
        config_ex = Exception("Unable to load config file (" + name + ".config). \n"
            "Have you remembered to copy/renamee one of the template files?")
        raise config_ex from ex

    return config


