# -*- coding: utf-8  -*-
# @Author: ty
# @File name: Utils.py 
# @IDE: PyCharm
# @Create time: 12/23/20 8:47 PM
import time

from settings import ALLOWED_EXTENSIONS

validation = {
    # 验证规则
    'required': {
        True: '必须',
        False: '非必须',
    },
    'type': '类型',
    'string': '字符串',
    'integer': '整型',
    'minlength': '最小长度',
    'maxlength': '最大长度',

    # 验证字段
    'nick_name': '昵称',
    'head_img': '头像',
    'email': '邮箱',
    'password': '密码',
}


class Utils():

    @staticmethod
    def list_to_dict(data):
        """
        sql结果列表对象类型转换为字典
        :param data:
        :return:
        """
        data_list = []
        for value in data:
            value = value.to_dict()
            data_list.append(value)
        data_dict = {}
        data_dict = data_list
        return data_dict

    @staticmethod
    def class_to_dict(obj):
        """
        sql结果对象类型转换为字典(支持单个对象,list, set)
        :param obj:
        :return:  dict
        """
        is_list = obj.__class__ == [].__class__
        is_set = obj.__class__ == set().__class__
        if is_list or is_set:
            obj_list = []
            for i in obj:
                dict = {}
                dict.update(i.__dict__)
                obj_list.append(dict)
                return obj_list
        else:
            dict = {}
            dict.update(obj.__dict__)
            return dict

    @staticmethod
    def allowed_file(filename):
        """
        验证文件类型
        :param filename:
        :return:
        """
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @staticmethod
    def unique_id(prefix=''):
        """
        uuid, 唯一id
        :param prefix:
        :return:
        """
        return prefix + hex(int(time.time()))[2: 10] + hex(int(time.time() * 1000000) % 0x100000)[2: 7]

    @staticmethod
    def validate_msg_format(name, rules, msg):
        """
        格式化验证错误描述
        :param name:
        :param rules:
        :param msg:
        :return:
        """
        if not msg:
            msg_format = dict()
            for key in rules:
                if key == 'required':
                    rule_msg = ''
                    action_msg = validation[key][rules[key]]
                elif key == 'maxlength':
                    rule_msg = validation[key]
                    action_msg = rules[key]
                elif key == 'minlength':
                    rule_msg = validation[key]
                    action_msg = rules[key]
                else:
                    rule_msg = validation[key]
                    action_msg = validation[rules[key]]
                msg_format[key] = '{} {} {}'.format(validation[name], rule_msg, action_msg)
            return msg_format
        return msg
