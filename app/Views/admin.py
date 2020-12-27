# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:59 PM
from flask import Blueprint

from app.Views.base import BaseView

admin = Blueprint('admin', __name__, static_folder='../../static', template_folder='../../templates')


@admin.route('/register')
def register():
    return BaseView().success_data(msg='注册成功')
