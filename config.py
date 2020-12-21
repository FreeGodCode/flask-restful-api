# # -*- coding: utf-8  -*-
# # @Author: ty
# # @File name: config.py
# # @IDE: PyCharm
# # @Create time: 12/21/20 5:02 PM
# import os
#
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#
#
# class Config():
#     DEBUG = True
#     SECRET_KEY = 'tycarry'
#     NAME = 'TY'
#     EMAIL = 'thechosenone_ty@163.com'
#
#
# class DevelopmentConfig(Config):
#     """开发环境"""
#     # database
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         'DEV_DATABASE_URI') or 'mysql+pymysql://root:123456@127.0.0.1:3306/dev-flask-restful-api?charset=utf8'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#
# class TestingConfig(Config):
#     """测试环境"""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         'TEST_DATABASE_URI') or 'mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#
# class ProductionConfig(Config):
#     """生产环境"""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         'DATABASE_URI') or 'mysql+pymysql://root:123456@127.0.0.1:3306/flask-restful-api?charset=utf8'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#
# env = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig,
# }
#
# # log save 1为文件形式, 2为数据库形式, 默认数据库形式
# SAVE_LOG = 1
# # 上传文件目录
# UPLOAD_DIR = [
#     os.path.join(BASE_DIR, '/uploads'),
# ]
# # 上传文件大小不超过10M
# MAX_CONTENT_LENGTH = 10 * 1024 * 1024
# # 允许上传文件格式
# ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
