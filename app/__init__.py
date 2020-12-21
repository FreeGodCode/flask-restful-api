# -*- coding: utf-8  -*-
# @Author: ty
# @File name: app.py 
# @IDE: PyCharm
# @Create time: 12/21/20 5:00 PM
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from utils.ExceptionApi import ExceptionApi

db = SQLAlchemy()
# 创建数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建session类型
DBSession = sessionmaker(bind=engine)
dbSession = DBSession()

app = Flask(__name__)
# 配置sqlalchemy 数据库驱动://用户名:密码@主机地址:端口号/数据库?编码方式
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICAIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# 上传文件配置
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 目录
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH  # 大小

from .. import environment

environment = environment.read()

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
    return ExceptionApi(Code.ERROR, e)


if environment == 'socket':
    # handles the default namespace
    @socketio.on_error_default
    def error_handler(e):
        return ExceptionApi(Code.ERROR, e)

# 引入使用的控制器
if environment == 'run' or environment == 'restful':
    app.register_blueprint(admin, url_prefix='/admin')

if environment == 'socket':
# 引入socketio控制层

# 在socket模式下使用后台线程作为计划任务
if environment == 'job':
    # 任务调度
    sched = BlockingScheduler()
    # 任务引入
    from app.Job import Cron, Interval
