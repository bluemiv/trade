# -*- coding: utf-8 -*-

import json
import os


def get_config(config_path=None):
    """config 파일을 읽어서 dictionary로 반환한다.

    Args:
        config_path: config 파일 전체 경로 (절대 경로 권장)
    """
    if config_path is not None:
        _config_path = os.path.abspath(config_path)
    else:
        _config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'config.json'))

    assert os.path.exists(_config_path), "Not found config.json. path: {}".format(_config_path)

    with open(_config_path, "rb") as f:
        config = f.read().decode('utf-8')
        config_dict = json.loads(config)

    return config_dict
