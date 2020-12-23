# -*- coding: utf-8  -*-
# @Author: ty
# @File name: Log.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:15 AM
import logging
import time


def log():
    logger = logging.getLogger('error_msg')
    logger.setLevel(logging.DEBUG)
    # 建立一个filehandler来记录日志文件,日志级别在debug以上
    log_file_name = logging.FileHandler(time.strftime('%Y-%m-%d', time.localtime()) + '.log')
    log_file_name.setLevel(logging.DEBUG)
    # 建立一个streamhandler将日志输出在CMD窗口,级别为error以上
    cmd_stream = logging.StreamHandler()
    cmd_stream.setLevel(logging.ERROR)
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_name.setFormatter(formatter)
    cmd_stream.setFormatter(formatter)
    # 将响应的handler添加到logger对象中
    logger.addHandler(log_file_name)
    logger.addHandler(cmd_stream)
    return logger