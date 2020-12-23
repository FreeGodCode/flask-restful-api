# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy_serializer import SerializerMixin

from app import dbSession
from app.Models.BaseModel import BaseModel
from app.Models.Model import HotImgShard


class ImgShard(HotImgShard, BaseModel, SerializerMixin):
    """"""
    @staticmethod
    def add(index, uuid, imgString):
        """
        增加分片数据
        :param index:
        :param uuid:
        :param imgString:
        :return:
        """
        data = ImgShard(index=index, uuid=uuid, imgString=imgString)
        dbSession.add(data)
        return dbSession.commit()

    @staticmethod
    def get_data(uuid):
        """
        根据uuid获取分片数据
        :param uuid:
        :return:
        """
        obj = dbSession.query(ImgShard).filter_by(uuid=uuid).order_by('index').all()
        data = Utils.db_to_d(obj)
        return data