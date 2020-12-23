# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:04 PM
import time

from sqlalchemy import event

from app.Models.Log import Log


@event.listens_for(Log, 'before_insert')
def log_before_insert(mapper, connection, target):
    target.create_time = int(time.time())
