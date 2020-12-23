# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy import desc, asc

from app import dbSession


class BaseModel():

    # def get_list(self, cls_: object, filters: set, order: str='id desc', field: tuple=(), offset: int=0, limit: int=10)-> dict:
    def get_list(self, cls_: object, filters=(), order='id desc', field=(), offset=0, limit=10):
        """
        列表
        :param cls_:
        :param filters:
        :param order:
        :param field:
        :param offset:
        :param limit:
        :return:
        """
        result = {}
        result['page'] = {}
        result['page']['count'] = dbSession.query(cls_).filter(*filters).count()
        result['list'] = []
        result['page']['total_page'] = self.get_page_number(result['page']['count'], limit)
        result['page']['current_page'] = offset
        if offset != 0:
            offset = (offset - 1) * limit

        if result['page']['count'] > 0:
            result['list'] = dbSession.query(cls_).filter(*filters)
            order_list = order.split(' ')
            if order_list[1] == 'desc':
                result['list'] = result['list'].order_by(desc(order_list[0])).offset(offset).limit(limit).all()
            else:
                result['list'] = result['list'].order_by(asc(order_list[0])).offset(offset).limit(limit).all()
        if not field:
            result['list'] = [res.to_dict() for res in result['list']]
        else:
            result['list'] = [res.to_dict(only=field) for res in result['list']]
        return result

    def get_all(self, cls_: object, filters: set, order: str = 'id desc', field: tuple = (), limit: int = 0) -> list:
        """
        查询全部
        :param cls_:
        :param filters:
        :param order:
        :param field:
        :param limit:
        :return:
        """
