import yaml
import logging
from Singleton.Singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self, path: str = 'config/config.yaml'):
        with open(path, 'r', encoding='UTF=8') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.error(exc)
                raise Exception(exc)
