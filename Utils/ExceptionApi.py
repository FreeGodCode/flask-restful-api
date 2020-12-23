# -*- coding: utf-8  -*-
# @Author: ty
# @File name: ExceptionApi.py 
# @IDE: PyCharm
# @Create time: 12/21/20 6:54 PM
import sys
import traceback

from flask import jsonify, make_response

from Utils.Log import log
from Utils.Utils import Utils
from app import dbSession
from app.Service.LogService import LogService
from settings import DEBUG_LOG, SAVE_LOG


def ExceptionApi(code, e):
    """
    接口异常处理
    :param code:
    :param e:
    :return:
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if DEBUG_LOG:
        # 文件形式
        if SAVE_LOG == 1:
            log().exception(e)
        # 数据库形式
        elif SAVE_LOG == 2:
            # 日志服务
            LogService().add(e, 1, 3)
    body = {}
    body['error_code'] = code
    body['error'] = True
    body['show'] = False
    body['debug_id'] = Utils.unique_id()
    dbSession.close()
    body['trackback'] = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return make_response(jsonify(body))
