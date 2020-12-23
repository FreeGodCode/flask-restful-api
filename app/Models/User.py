# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy import desc, asc
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from Utils.Decorator import classTransaction
from app import dbSession
from app.Models.BaseModel import BaseModel
from app.Models.Model import HotUser


class User(HotUser, BaseModel, SerializerMixin):

    serialize_rules = ('-password', )
    def __repr__(self):
        return 'User(id="%s")' % self.id

    def get_one(self, filters, order='id desc', field=()):
        """
        获取一条
        :param filters:
        :param order:
        :param field:
        :return:
        """
        result = dbSession.query(User).filter(*filters)
        # 查询结果为空
        if result == None:
            return None
        order_list = order.split(' ')
        # 查询结果降序排列
        if order_list[1] == 'desc':
            result = result.order_by(desc(order_list[0])).first()
        # 查询结果升序排列
        else:
            result = result.order_by(asc(order_list[0])).first()
        # 查询字段为空
        if not field:
            result = result.to_dict()
        else:
            result = result.to_dict(only=field)
        return result

    @staticmethod
    def set_password(password):
        """
        密码加密
        :param password:
        :return:
        """
        return generate_password_hash(password)

    @staticmethod
    def check_password(hash_password, password):
        """
        校验密码
        :param hash_password:
        :param password:
        :return:
        """
        return check_password_hash(hash_password, password)

    @staticmethod
    def get(id):
        """
        获取用户信息
        :param id:
        :return:
        """
        return dbSession.query(User).filter_by(id=id).first()

    @classTransaction
    def add(self, user):
        """
        增加用户
        :param id:
        :return:
        """
        dbSession.add(user)
        return True

    def delete(self, id):
        """
        根据id删除用户
        :param id:
        :return:
        """
        dbSession.query(User).filter_by(id=id).delete()
        return dbSession.commit()

    @staticmethod
    def update(email, updated_time):
        """
        更新更新时间
        :param email:
        :param updated_time:
        :return:
        """
        dbSession.query(User).filter_by(email=email).update({'updated_time': updated_time})
        return dbSession.commit()
