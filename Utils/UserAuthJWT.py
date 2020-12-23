# -*- coding: utf-8  -*-
# @Author: ty
# @File name: UserAuthJWT.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:30 AM
import datetime
import time

import jwt

from app.Models.User import User
from settings import JWT_LEEWAY, SECRET_KEY


class UserAuthJWT():
    """JWT工具函数"""

    @staticmethod
    def encode_auth_token(user_id, updated_time):
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
                    'updated_time': updated_time,
                }
            }
            return jwt.JWT.encode(payload=payload, key=SECRET_KEY, alg='HS256')
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
            # payload = jwt.JWT.decode(auth_token, key=SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            payload = jwt.JWT.decode(auth_token, SECRET_KEY)
            if 'data' in payload and 'id' in payload['data']:
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
        user_info = User().get_one(filters)
        user_info_password = User().get_one(filters, order='id desc', field=('password',))
        if user_info is None:
            return BaseController().error('找不到用户')
        else:
            if User.check_password(user_info_password['password'], password):
                updated_time = int(time.time())
                User.update(email=email, updated_time=updated_time)
                token = UserAuthJWT.encode_auth_token(user_info['id'], updated_time)
                return BaseController().successData({'token': token.decode(), 'user': user_info}, '登录成功')
            else:
                return BaseController().error('密码不正确')


def identify(self, request):
    """
    用户鉴权
    :param request:
    :return:
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token_list = auth_header.split(' ')
        if not auth_token_list or auth_token_list[0] != 'JWT' or len(auth_token_list) != 2:
            return '请传递正确的验证头信息'
        else:
            auth_token = auth_token_list[1]
            payload = self.docode_auth_token(auth_token)
            if not isinstance(payload, str):
                user = User.get(payload['data']['id'])
                if user is None:
                    return '找不到用户信息'
                else:
                    if user.updated_time == payload['data']['update_time']:
                        result = payload
                    else:
                        return 'Token已更改,请重新登录获取Token'
            else:
                result = payload
    else:
        return '没有提供认证token'
    return result
