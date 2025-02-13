import yaml
def load_config(yaml_file="../config/source-target.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config
