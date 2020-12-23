# -*- coding: utf-8  -*-
# @Author: ty
# @File name: LogService.py 
# @IDE: PyCharm
# @Create time: 12/23/20 10:30 PM
from Utils.Decorator import classTransaction
from app import dbSession
from app.Models.User import User


class TableService():
    @classTransaction
    def lock(self):
        """
        行级锁
        :return:
        """
        query = dbSession.query(User).filter(User.id == 34).with_for_update().first()
        dbSession.execute('select sleep(10)')
