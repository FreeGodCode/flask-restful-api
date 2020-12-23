# -*- coding: utf-8  -*-
# @Author: ty
# @File name: Decorator.py 
# @IDE: PyCharm
# @Create time: 12/22/20 5:12 PM
# 装饰器定义
import json
from functools import wraps

import cerberus as cerberus
from flask import request, make_response

from Code import Code
from app import dbSession


def transaction(func):
    """
    不用于类方法的事务装饰器
    :param func:
    :return: func|False
    """

    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            dbSession.commit()
            return result
        except Exception as e:
            dbSession.rollback()
            raise e

    return inner_wrapper


def classTransaction(func):
    """
    用于类方法的事务装饰器
    :param func:
    :return: func|False
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            dbSession.commit()
            return result
        except Exception as e:
            dbSession.rollback()
            raise e

    return wrapper


def validateInputByName(name, rules, error_msg=dict(), default=''):
    """
    根据字段名验证输入信息
    请求参数都会被格式化为string, 无法使用int去验证
    :param name:  string
    :param rules:  dict
    :param error_msg: string
    :param default:  string
    :return:  response
    """
    if name == 'error':
        error = {}
        error['msg'] = '不能使用error关键字作为请求参数'
        error['error_code'] = Code.SERVER_INTERNAL_ERROR
        error['error'] = True
        return error
    # cerberus一个轻量级的可扩展的python数据验证库
    v = cerberus.Validator(rules, error_handler=CustomErrorHandler(custom_messages=error_msg))
    try:
        requests = request.values()
    except TypeError:
        requests = request.get_json()

    if name not in requests:
        requests['name'] = default
    cookedReqVal = {'name': requests['name']}
    if (v.vaildate(cookedReqVal)):
        return requests

    error = {}
    error['msg'] = v.errors
    error['error_code'] = Code.SERVER_INTERNAL_ERROR
    error['error'] = True
    return error


def validator(name, rules, msg=dict(), defalut=''):
    """
    装饰器:函数的嵌套,内层函数使用外层函数的变量,外层函数返回内层函数的引用
    :param name: 字段名
    :param rules:  规则
    :param msg:  描述
    :param defalut:
    :return:  func|json
    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            msgFormat = Utils.validateMsgFormat(name, rules, msg)
            error = validateInputByName(name, {name: rules}, {name: msgFormat}, default=defalut)
            if 'error' in error:
                return make_response(json.dumps(error))
            if 'params' in kwargs.keys():
                kwargs['params'][name] = error[name]
                kwargs = kwargs['params']
            else:
                kwargs = error
            return func(kwargs)

        return inner_wrapper

    return wrapper
