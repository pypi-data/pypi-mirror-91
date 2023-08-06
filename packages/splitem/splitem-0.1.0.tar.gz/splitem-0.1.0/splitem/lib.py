import os
import yaml


def read_target(target: str) -> any:
    real_target = os.path.abspath(target)
    manifests = {}
    if os.path.isfile(real_target):
        f = open(target, 'r')
        manifests = yaml.load_all(f)
    else:
        raise FileNotFoundError
    return manifests
