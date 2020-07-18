#!/usr/bin/env python

import yaml
import os
import logging

global config_dict

# 获取当前项目根目录
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../../"
base_dir = os.path.abspath(project_path)

with open(base_dir + "/config.yml", 'r') as stream:
    try:
        config_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)


def get_config_dict():
    return config_dict


def get_value(key, defValue=None):
    """
    获得一个全局变量,不存在则返回默认值
    """
    try:
        return config_dict[key]
    except KeyError:
        return defValue
