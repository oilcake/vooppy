import yaml

import os

CONFIG = "./interface-config.yml"

dirname = os.path.dirname(__file__)
config = os.path.join(dirname, CONFIG)


def config_parser(config):
    with open(config, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


print(config_parser(config))
