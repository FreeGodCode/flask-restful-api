# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy import desc, asc
from sqlalchemy_serializer import SerializerMixin

from Utils.Decorator import classTransaction
from app import dbSession
from app.Models.BaseModel import BaseModel
from app.Models.Model import HotLog


class Log(HotLog, BaseModel, SerializerMixin):
    """"""

    def get_one(self, filters, order='id desc', field=()):
        """

        :param filters:
        :param order:
        :param field:
        :return:
        """
        result = dbSession.query(Log).filter(*filters)
        order_list = order.split(' ')
        if result == None:
            return None
        if order_list[1] == 'desc':
            result = result.order_by(desc(order[0])).first()
        else:
            result = result.order_by(asc(order_list[0])).first()
        if not field:
            result = result.to_dict()
        else:
            result = result.to_dict(only=field)

        return result

    @classTransaction
    def add(self, data):
        """
        添加
        :param data:
        :return:
        """
        log = Log(**data)
        dbSession.add(log)
        dbSession.flush()
        return log.id
