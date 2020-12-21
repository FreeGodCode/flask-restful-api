# -*- coding: utf-8  -*-
# @Author: ty
# @File name: environment.py 
# @IDE: PyCharm
# @Create time: 12/21/20 6:02 PM
import json
import os


def init(name):
    """
    初始化运行环境
    :param name:
    :return:
    """
    path = os.getcwd() + '/environment.json'
    data = {'environment': name}
    with open(path, 'w+') as f:
        f.write(json.dumps(data))


def read():
    """
    读取环境变量
    :return: dict environment
    """
    with open(os.getcwd() + '/environment.json', 'r') as f:
        environment = json.loads(f.read())['environment']
        return environment
