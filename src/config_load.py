import yaml

def load(config_path='config.yml'):
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)


# Load the configuration at the start of your script
config = load()
