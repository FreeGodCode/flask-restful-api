# -*- coding: utf-8  -*-
# @Author: ty
# @File name: CustomErrorHandler.py 
# @IDE: PyCharm
# @Create time: 12/23/20 11:06 AM
import cerberus
from cerberus import errors


class CustomErrorHandler(errors.BasicErrorHandler):
    """"""

    def __init__(self, tree=None, custom_messages=None):
        super(CustomErrorHandler, self).__init__(tree)
        self.custom_messages = custom_messages

    def format_message(self, field, error):
        temp = self.custom_messages
        for i in error.schema_path:
            try:
                temp = temp[i]
            except KeyError:
                return super(CustomErrorHandler, self)._format_message(field, error)
        if isinstance(temp, dict):
            return super(CustomErrorHandler, self)._format_message(field, error)
        else:
            return temp
