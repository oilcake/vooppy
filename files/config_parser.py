import yaml

config = '/Users/Oilcake/Documents/Dev/vooppy/interface-config.yml'

with open(config, "r") as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
