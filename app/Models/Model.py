# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
from sqlalchemy import Column, Integer, String, FetchedValue, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class HotComment(Base):
    """评论模型类"""
    __tablename__ = 'db_hot_comment'
    id = Column(Integer, primary_key=True)
    msg = Column(String(128), nullable=False, server_default=FetchedValue())
    user_id = Column(Integer)
    article_id = Column(Integer, nullable=False)
    add_time = Column(Integer, nullable=False)


class HotImgShard(Base):
    """头像模型类"""
    __tablename__ = 'db_hot_img_shard'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, server_default=FetchedValue())
    imgString = Column(Text, nullable=False)
    index = Column(Integer, nullable=False)


class HotLog(Base):
    """日志模型类"""
    __tablename__ = 'db_hot_log'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, server_default=FetchedValue())
    level = Column(Integer, nullable=False, server_default=FetchedValue())
    data = Column(Text, nullable=False)
    create_time = Column(Integer, nullable=False)


class HotSuggest(Base):
    """建议模型类"""
    __tablename__ = 'db_hot_suggest'
    id = Column(Integer, primary_key=True)
    add_time = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message = Column(String(256, 'utf8_unicode_ci'), nullable=False)


class HotUser(Base):
    """用户模型类"""
    __tablename__ = 'db_hot_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128, 'utf8_unicode_ci'), unique=True)
    email = Column(String(128, 'urf8_unicode_ci'), nullable=False, unique=True)
    telphone = Column(String(32, 'utf8_unicode_ci'), unique=True)
    password = Column(String(128, 'utf8_unicode_ci', nullable=False))
    status = Column(Integer, nullable=False)
    token = Column(String(128, 'utf8_unicode_ci'))
    created_time = Column(Integer)
    updated_time = Column(Integer)
    url_path = Column(String(256, 'utf8_unicode_ci'))
    real_path = Column(String(256, 'utf8_unicode_ci'))
