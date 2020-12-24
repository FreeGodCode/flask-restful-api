# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:59 PM
import json

import cerberus
from flask import request, jsonify

from Code import Code
from Utils.CustomErrorHandler import CustomErrorHandler
from Utils.Log import log
from Utils.Utils import Utils
from app.Service.LogService import LogService
from settings import DEBUG_LOG, SAVE_LOG


class BaseView():
    """"""

    def validate_input(self, rules, error_msg=None):
        """
        验证输入信息
        :param rules:
        :param error_msg:
        :return:
        """
        v = cerberus.Validator(rules, error_handler=CustomErrorHandler(custom_messages=error_msg))
        try:
            requests = request.values()
        except TypeError:
            requests = request.get_json()
        if v.validate(requests):
            return True

        error = {}
        error['msg'] = v.errors
        error['error_code'] = Code.BAD_REQUEST
        error['error'] = True
        return self.json(error)

    def validate_input_by_name(self, name, rules, error_msg=None):
        """
        根据字段名验证输入信息
        :param name:
        :param rules:
        :param error_msg:
        :return:
        """
        v = cerberus.Validator(rules, error_handler=CustomErrorHandler(custom_messages=error_msg))
        try:
            requests = request.values()
        except TypeError:
            requests = request.get_json()
        if v.validate({name: requests[name]}):
            return requests
        error = {}
        error['msg'] = v.errors
        error['error_code'] = Code.BAD_REQUEST
        error['error'] = True
        return self.json(error)

    def json(self, body={}):
        """
        返回json数据
        :param body:
        :return:
        """
        if DEBUG_LOG:
            debug_id = Utils.unique_id()
            data = {
                'LOG_ID': debug_id,
                'IP_ADDRESS': request.remote_addr,
                'REQUEST_URL': request.url,
                'REQUEST_METHOD': request.method,
                'PARAMETERS': request.args,
                'RESPONSE': body,
            }
            # 以文件形式保存日
            if SAVE_LOG == 1:
                log().debug(data)
            elif SAVE_LOG == 2:
                LogService().add(json.dumps(data), 1, 2)
        body['debug_id'] = debug_id
        return jsonify(body)

    def error(self, msg='', show=True):
        """返回错误信息"""
        return self.json({'error_code': Code.BAD_REQUEST, 'error': True, 'msg': msg, 'show': show})

    def success_data(self, data='', msg='', show=True):
        """
        返回成功信息
        :param data:
        :param msg:
        :param show:
        :return:
        """
        return self.json({'error_code': Code.SUCCESS, 'data': data, 'msg': msg, 'show': show})
