# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:13 PM
import re

from flask import request, make_response, jsonify

from app import app


@app.before_request
def XSSProtection():
    """
    中间件,xss保护,响应后前端模板进行过滤
    :return:
    """
    data = re.compile(r'<[^>]+>', re.S)
    for (k, v) in request.args.items():
        if re.search(data, v) is not None:
            return make_response(jsonify({'error_code': 400, 'error': True, 'msg': '请不要使用HTML标签'}))
