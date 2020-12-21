# -*- coding: utf-8  -*-
# @Author: ty
# @File name: settings.py 
# @IDE: PyCharm
# @Create time: 12/21/20 6:34 PM
# sqlalchemy配置
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# sqlalchemy settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask-restful-api?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# debug
DEBUG_LOG = True
# log save 1 为文件形式, 2 为数据库形式,默认数据库形式
SAVE_LOG = 1

# upload folder path settings
UPLOAD_FOLDER = [
    os.path.join(BASE_DIR, 'uploads')
]
# 上传文件大小不超过10M
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
# 允许上传文件格式
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

