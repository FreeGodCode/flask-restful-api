# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy.orm import relationship, foreign, remote
from sqlalchemy_serializer import SerializerMixin

from app import dbSession
from app.Models.BaseModel import BaseModel
from app.Models.Model import HotSuggest
from app.Models.User import User


class Suggest(HotSuggest, BaseModel, SerializerMixin):
    user = relationship('User', uselist=False, primaryjoin=foreign(HotSuggest.user_id) == remote(User.id))

    @staticmethod
    def one_to_many():
        """
        一对多普通方式
        :return:
        """
        data = dbSession.query(Suggest).filter(User.id == Suggest.user_id).all()
        data_msg = Utils.db_1_to_d(data)
        return data_msg

    @staticmethod
    def join():
        """
        一对多join方式
        :return:
        """
        data = dbSession.query(Suggest).join(User, User.id == Suggest.user_id).all()
        data_msg = Utils.db_1_to_d(data)
        return data_msg

    @staticmethod
    def left_join():
        """
        一对多left join 方式
        :return:
        """
        data = dbSession.query(Suggest).outerjoin(User, User.id == Suggest.user_id).all()
        data_msg = Utils.db_1_to_d(data)
        return data_msg