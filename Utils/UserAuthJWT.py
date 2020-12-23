# -*- coding: utf-8  -*-
# @Author: ty
# @File name: UserAuthJWT.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:30 AM
import datetime

import jwt

from settings import JWT_LEEWAY, SECRET_KEY


class UserAuthJWT():
    """JWT工具函数"""

    @staticmethod
    def encode_auth_token(user_id, updated_at):
        """
        生成认证token
        :param user_id: int
        :param updated_at: login_time int timestamp
        :return:  string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_LEEWAY),
                'iat': datetime.datetime.utcnow(),
                'iss': '',
                'ken': '',
                'data': {
                    'id': user_id,
                    'updated_at': updated_at,
                }
            }
            return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return:  integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    @staticmethod
    def authenticate(email, password):
        """
        用户登录,登录成功返回token,并且将登录时间写入数据库,登录失败返回失败原因
        :param email:
        :param password:
        :return: json
        """
        filters = {
            User.email == email
        }
        userinfo = User().getOne(filters)
        user

