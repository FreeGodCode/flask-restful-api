# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
import math

from sqlalchemy import desc, asc

from Code import Code
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
        :param cls_: 数据库模型实体类
        :param filters: 查询条件
        :param order: 排序
        :param field: 字段
        :param limit: 取多少条
        :return: dict
        """
        if not filters:
            result = dbSession.query(cls_)
        else:
            result = dbSession.query(cls_).filter(*filters)
        order_list = order.split(' ')
        if order_list[1] == 'desc':
            result = result.order_by(desc(order_list[0])).all()
        else:
            result = result.order_by(asc(order_list[0])).all()
        if not field:
            result = [res.to_dict() for res in result]
        else:
            result = [res.to_dict(only=field) for res in result]
        return result

    def get_one(self, cls_: object, filters: set, order: str = 'id desc', field: tuple = ()):
        """
        获取一条
        :param cls_: 数据库模型实体类
        :param filters: 查询条件
        :param order: 排序方式
        :param field: 查询字段
        :return:  dict
        """
        result = dbSession.query(cls_).filter(*filters)
        order_list = order.split(' ')
        if result == None:
            return None
        # 排序方式为降序
        if order_list[1] == 'desc':
            result = result.order_by(desc(order_list[0])).first()
        else:
            result = result.order_by(asc(order_list[0])).first()
        if not field:
            result = result.to_dict()
        else:
            result = result.to_dict(only=field)
        return result

    def add(self, cls_, data: dict) -> int:
        """
        添加
        :param cls_: 数据库模型实体类
        :param data:  数据
        :return:  bool
        """
        user = cls_(**data)
        dbSession.add(user)
        dbSession.flush()
        return user.id

    def edit(self, cls_: object, data: dict, filters: set) -> bool:
        """
        修改
        :param cls_: 数据库模型实体类
        :param data: 数据
        :param filters:  筛选条件
        :return:  bool
        """
        return dbSession.query(cls_).filter(*filters).update(data, synchronize_session=False)

    def delete(self, cls_: object, filters: set) -> int:
        """
        删除
        :param cls_: 数据库模型实体类
        :param filters:  查询条件
        :return:  int(删除的数据id)
        """
        return dbSession.query(cls_).filter(*filters).delete(synchronize_session=False)

    def get_count(self, cls_: object, filters: set, field=None) -> int:
        """
        统计数据
        :param cls_: 数据模型实体类
        :param filters:  查询条件
        :param field:  查询字段
        :return:  int统计记录数量
        """
        if field == None:
            return dbSession.query(cls_).filter(*filters).count()
        else:
            return dbSession.query(cls_).filter(*filters).count(field)

    @staticmethod
    def get_page_number(count: int, page_size: int) -> int:
        """
        获取总页数
        :param count: 记录条数
        :param page_size: 没页显示条数
        :return:  int总页数
        """
        page_size = abs(page_size)
        if page_size != 0:
            total_page = math.ceil(count / page_size)
        else:
            total_page = math.ceil(count / 5)
        return total_page

    @staticmethod
    def format_paged(page, size, total):
        """
        格式化分页
        :param page: int
        :param size: int
        :param total:  int
        :return: dict
        """
        if int(total) > int(page) * int(size):
            more = 1
        else:
            more = 0
        return {
            'total': int(total),
            'page': int(page),
            'size': int(size),
            'more': more,
        }

    @staticmethod
    def format_body(data={}, msg='', show=True):
        """
        格式化返回体
        :param data:
        :param msg:
        :param show:
        :return:
        """
        dataformat = {}
        dataformat['error_code'] = Code.SUCCESS
        dataformat['data'] = data
        dataformat['msg'] = msg
        dataformat['show'] = show
        return dataformat

    @staticmethod
    def format_error(code, message='', show=True):
        """
        格式化错误返回体
        :param code:
        :param message:
        :param show:
        :return:
        """
        if code == Code.BAD_REQUEST:
            message = 'Bad request.'
        elif code == Code.PAGE_NOT_FOUND:
            message = 'NO result matched.'

        body = {}
        body['error'] = True
        body['error_code'] = Code.BAD_REQUEST
        body['msg'] = message
        body['show'] = show
        return body
