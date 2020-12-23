# -*- coding: utf-8  -*-
# @Author: ty
# @File name: LogService.py 
# @IDE: PyCharm
# @Create time: 12/23/20 10:30 PM
import time

from app import dbSession
from app.Models.Model import HotLog


class LogService():
    """日志服务层"""

    def add(self, data, type=1, level=1):
        """
        添加
        :param data:
        :param type:
        :param level:
        :return:
        """
        data_dict = {
            'data': data,
            'type': type,
            'level': level,
            'create_time': int(time.time())
        }
        try:
            log = HotLog(**data_dict)
            dbSession.add(log)
            dbSession.flush()
            id = log.id
            dbSession.commit()
            return id
        except Exception as e:
            dbSession.rollback()
            return 0
