# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
import math

from sqlalchemy_serializer import SerializerMixin

from app import dbSession
from app.Models.BaseModel import BaseModel
from app.Models.Model import HotComment


class Comment(HotComment, BaseModel, SerializerMixin):
    """"""
    serialize_rules = ('update_time', '-add_time')

    # def __setattr__(self, *args, **kwargs):
    #     args[1].class_.add_time = 1
    #     return object.__setattr__(self, *args, **kwargs)

    @property
    def update_time(self):
        """
        更新时间
        :return:
        """
        update = self.add_time
        return update

    def get_comment_list(self, page, per_page):
        """
        批量获取
        :param page:
        :param per_page:
        :return:
        """
        data = self.get_list({}, Comment.add_time.desc(), (), page, per_page)
        return data

    def get_list(self, filters, order, field=(), offset=0, limit=10):
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
        result['page']['count'] = dbSession.query(Comment).filter(*filters).count()
        result['list'] = []
        result['page']['total_page'] = self.get_page_number(result['page']['count'], limit)
        result['page']['current_page'] = offset
        if offset != 0:
            offset = (offset - 1) * limit

        if result['page']['count'] > 0:
            result['list'] = dbSession.query(Comment).filter(*filters)
            result['list'] = result['list'].order_by(order).offset(offset).limit(limit).all()

        if not field:
            result['list'] = [res.to_dict() for res in result['list']]
        else:
            result['list'] = [res.to_dict(only=field) for res in result['list']]

        return result

    @staticmethod
    def get_page_number(count, page_size):
        """
        获取总页数
        :param count:
        :param page_size:
        :return:
        """
        count = float(count)
        page_size = abs(page_size)
        if page_size != 0:
            total_page = math.ceil(count / page_size)
        else:
            total_page = math.ceil(count / 5)
        return total_page
