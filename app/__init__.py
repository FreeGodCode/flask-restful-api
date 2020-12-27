# -*- coding: utf-8  -*-
# @Author: ty
# @File name: app.py 
# @IDE: PyCharm
# @Create time: 12/21/20 5:00 PM
import json
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from Code import Code
from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from Utils.ExceptionApi import ExceptionApi
from .Views.admin import admin

# db = SQLAlchemy()
# 创建数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建session类型
DBSession = sessionmaker(bind=engine)
dbSession = DBSession()

app = Flask(__name__, static_folder='../../static', template_folder='../../templates')
# 配置sqlalchemy 数据库驱动://用户名:密码@主机地址:端口号/数据库?编码方式
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# 跟踪数据库的修改,不建议开启,消耗性能,在未来的版本中会被移除
app.config['SQLALCHEMY_TRACK_MODIFICAIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# 上传文件配置
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 目录
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH  # 大小

from .. import environment

environment = environment.read()
# with open(os.getcwd() + '/environment.json', 'r') as f:
#     environment = json.loads(f.read())['environment']
# 实例化websocket
async_mode = 'gevent'
socketio = SocketIO(app, async_mode=async_mode)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """

    :param exception:
    :return:
    """
    dbSession.close()


# 挂在500异常处理,并记录日志
@app.errorhandler(Exception)
def error_handler(e):
    return ExceptionApi(Code.SERVER_INTERNAL_ERROR, e)


if environment == 'socket':
    # handles the default namespace
    @socketio.on_error_default
    def error_handler(e):
        return ExceptionApi(Code.SERVER_INTERNAL_ERROR, e)

# 引入使用的控制器
if environment == 'run' or environment == 'restful':
    app.register_blueprint(admin, url_prefix='/admin')

if environment == 'socket':
    # 引入socketio控制层
    from app.Views import socket

from app.Models.Log import Log


# 引入数据库事件
# from app.Event import log
@event.listens_for(Log, 'before_insert')
def log_before_insert(mapper, connection, target):
    target.create_time = int(time.time())


# 在socket模式下使用后台线程作为计划任务
if environment == 'job':
    # 任务调度, 定时任务
    scheduler = BlockingScheduler()


    # 任务引入
    # from app.Job import cron, interval
    # 定时任务,使用cron触发类型,并使用装饰器实现,循环执行,每隔5秒钟执行一次
    @scheduler.scheduled_job('cron', second=5)
    def interval_job():
        print('<cron_job>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


    # 定时任务,使用interval触发类型,并使用装饰器实现,循环执行,每隔5秒钟执行一次
    @scheduler.scheduled_job('interval', second=5)
    def interval_job():
        print('<interval_job>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
