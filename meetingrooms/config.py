import json
import pathlib

def get_config_path(name):
    directory = pathlib.Path(__file__).resolve().parent
    config_file_path = directory.joinpath(name + '.config')
    return str(config_file_path)

def get_config(name):
    config_path = get_config_path(name)
    try:
        with open(config_path) as json_file:
            config = json.load(json_file)
    except:
        print("Unable to load config file (" + name + ".config).")
        print("Have you remembered to copy/renamee one of the template files?")
        raise

    return config


