import configparser
import os

def init_config(config_path = '../config/config.ini'):
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, config_path)
    config.read(config_path, encoding='utf-8')
    return config