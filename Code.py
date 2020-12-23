# -*- coding: utf-8  -*-
# @Author: ty
# @File name: Code.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:49 PM
class Code:
    """HTTP响应状态码定义"""
    SUCCESS = 200
    BAD_REQUEST = 400
    PAGE_NOT_FOUND = 404
    SERVER_INTERNAL_ERROR = 500

    ERROR_AUTH_CHECK_TOKEN_FAIL = 10001
    ERROR_AUTH_CHECK_TOKEN_TIMEOUT = 10002
    ERROR_AUTH_TOKEN = 10003
    ERROR_AUTH = 10004
