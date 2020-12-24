# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:59 PM
import base64
import os

from flask import request
from werkzeug.utils import secure_filename

from Utils.Decorator import validator
from Utils.UserAuthJWT import UserAuthJWT
from Utils.Utils import Utils
from app import app
from app.Models.Comments import Comment
from app.Models.ImgShard import ImgShard
from app.Models.Log import Log
from app.Models.Suggest import Suggest
from app.Models.User import User
from app.Service.TableService import TableService
from app.Views.base import BaseView


@app.route('/', methods=['GET'])
def index():
    """
    测试
    :return:
    """
    Log().add({
        'type': 1,
        'level': 1,
        'data': '1',
    })
    return BaseView().success_data(msg='启动成功')


@app.route('/api/lock_table', methods=['GET'])
def lock_table():
    TableService().lock()
    return BaseView().success_data(msg='加锁成功')


@app.route('/api/register', methods=['POST'])
@validator(name='email', rules={'required': True, 'type': 'string', 'minlength': 10, 'maxlength': 20})
@validator(name='password', rules={'required': True, 'type': 'string', 'minlength': 6, 'maxlength': 20})
def register(params):
    """
    注册
    :param params:
    :return:
    """
    filters = {
        User.email == params['email']
    }
    user = User().get_one(filters)
    if not user:
        user = User(email=params['email'], password=User.set_password(params['password']), status=1)
        status = user.add(user)
        if status == True:
            return BaseView().success_data(msg='注册成功')
        return BaseView().error('注册失败')
    return BaseView().error('帐号已注册')


@app.route('/api/login', methods=['GET'])
def login():
    """
    登录
    :return:
    """
    # email = request.args.get('email')
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return BaseView().error('用户名和密码不能为空')
    else:
        result = UserAuthJWT.authenticate(email, password)
        return result


@app.route('/api/user', methods=['GET'])
def get_user():
    """
    获取用户信息
    :return:
    """
    result = UserAuthJWT().identify(request)
    if isinstance(result, str):
        return BaseView().error(result)
    if result['data']:
        user = User.get(result['data']['id'])
        user_dict = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'login_time': user.updated_time,
        }
        return BaseView().success_data(user_dict)
    return BaseView().error('为找到用户')


@app.route('/api/user_info', methods=['POST'])
def get_user_info():
    """
    不通过鉴定权限获取用户信息
    :return:
    """
    id = request.args.get('id')
    data_list = User.query.filter_by(id=id).all()
    data_dict = Utils.list_to_dict(data_list)
    return BaseView().success_data(data_dict)


@app.route('/api/user_suggest', methods=['GET'])
def user_suggest():
    '''
    查询用户留言记录,一对多
    :return:
    '''
    data_msg = Suggest.one_to_many()
    return BaseView().success_data(data_msg)


@app.route('/api/user_suggest_join', methods=['GET'])
def user_suggest_join():
    """
    联合查询
    :return:
    """
    data_msg = Suggest.join()
    return BaseView().success_data(data_msg)


@app.route('/api/user_suggest_left', methods=['GET'])
def user_suggest_left():
    """
    left join
    如果想使用right join, 把类的顺序交换一下即可
    :return:
    """
    data_msg = Suggest.left_join()
    return BaseView().success_data(data_msg)


@app.route('/api/upload_document', methods=['POST'])
def upload_document():
    """
    上传文件并验证
    :return:
    """
    files = request.files['document']
    filename = secure_filename(files.filename)
    if files and Utils.allowed_file(filename):
        path = os.getcwd() + '/uploads/' + filename
        files.save(path)
        return BaseView().error('文件上传成功')
    return BaseView().error('文件类型错误')


@app.route("/api/upload_base64_document", methods=['POST'])
def upload_base64_document():
    """
    上传base64格式的文件,文件类型由前端传递
    :return:
    """
    rules = {
        'userImgOne': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'name': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'size': {
                    'required': True,
                    'type': 'integer',
                    'minlength': 2
                },
                'type': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                }
            }
        },
        'userImgTwo': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'name': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'size': {
                    'required': True,
                    'type': 'integer',
                    'minlength': 2
                },
                'type': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                }
            }
        },
        'userImgThree': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'name': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                },
                'size': {
                    'required': True,
                    'type': 'integer',
                    'minlength': 2
                },
                'type': {
                    'required': True,
                    'type': 'string',
                    'minlength': 2
                }
            }
        }
    }
    error_msg = {
        'userImgOne': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': '图一是必须的',
                    'type': '图一必须是字符串',
                    'minlength': '图一字符最小为2'
                },
                'name': {
                    'required': '图一是必须的',
                    'type': '图一的类型必须时字符串',
                    'minlength': '图一字符最小为2'
                },
                'size': {
                    'required': '图一是必须的',
                    'type': '图一的类型必须时字符串',
                    'minlength': '图一字符最小为2'
                },
                'type': {
                    'required': '图一是必须的',
                    'type': '图一的类型必须时字符串',
                    'minlength': '图一字符最小为2'
                }
            }
        },
        'userImgTwo': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': '图二是必须的',
                    'type': '图二的类型必须时字符串',
                    'minlength': '图二字符最小为2'
                },
                'name': {
                    'required': '图二是必须的',
                    'type': '图二的类型必须时字符串',
                    'minlength': '图二字符最小为2'
                },
                'size': {
                    'required': '图二是必须的',
                    'type': '图二的类型必须时字符串',
                    'minlength': '图二字符最小为2'
                },
                'type': {
                    'required': '图二是必须的',
                    'type': '图二的类型必须时字符串',
                    'minlength': '图二字符最小为2'
                }
            }
        },
        'userImgThree': {
            'type': 'dict',
            'schema': {
                'imgBase64': {
                    'required': '图三是必须的',
                    'type': '图三必须是字符串',
                    'minlength': '图三字符最小为2'
                },
                'name': {
                    'required': '图三是必须的',
                    'type': '图三必须是字符串',
                    'minlength': '图三字符最小为2'
                },
                'size': {
                    'required': '图三是必须的',
                    'type': '图三必须是字符串',
                    'minlength': '图三字符最小为2'
                },
                'type': {
                    'required': '图三是必须的',
                    'type': '图三必须是字符串',
                    'minlength': '图三字符最小为2'
                }
            }
        }
    }
    error = BaseView().validate_input(rules, error_msg)
    if error is not True:
        return error

    for k, v in request.json.items():
        user_info = v['imgBase64'].split[','][1]
        img_data = base64.b64decode(user_info)
        path = os.getcwd() + '/uploads/' + Utils.unique_id() + '.jpg'
        with open(path, 'wb') as f:
            f.write(img_data)
        return BaseView().success_data(msg='图片提交成功')


@app.route('/api/get_comments', methods=['POST'])
def get_comments():
    rules = {
        'pageNo': {
            'required': True,
            'type': 'integer'
        },
        'pageSize': {
            'required': True,
            'type': 'integer'
        }
    }
    error_msg = {
        'pageNo': {
            'required': '当前页必须',
            'type': '当前页页码必须为整数'
        },
        'pageSize': {
            'required': '当前页必须',
            'type': '当前页页码必须为整数'
        }
    }
    error = BaseView().validate_input(rules, error_msg)
    if error is not True:
        return error
    page = request.json.get('pageNo')
    per_page = request.json.get('pageSize')
    data = Comment().get_comment_list(page, per_page)
    return BaseView.json(data)


@app.route('/api/save_imgShard', methods=['POST'])
def save_imgShard():
    """
    接收图片分片数据并存入数据库
    :return:
    """
    rules = {
        'index': {
            'required': True,
            'type': 'integer',
        },
        'uuid': {
            'required': True,
            'type': 'string'
        },
        'imgString': {
            'required': True,
            'type': 'string'
        }
    }
    error_msg = {
        'index': {
            'required': '图片索引必须有',
            'type': '图片索引必须为字符串',
        },
        'uuid': {
            'required': '唯一id必须有',
            'type': '唯一id为字符串'
        },
        'imgString': {
            'required': '图片描述必须有',
            'type': '图片描述为字符串'
        }
    }
    error = BaseView().validate_input(rules, error_msg)
    if error is not True:
        return error
    index = request.json.get('index')
    uuid = request.json.get('uuid')
    imgString = request.json.get('imgString')
    data = ImgShard.add(index, uuid, imgString)
    if data:
        return BaseView().success_data(data=0, msg='图片分片提交成功')
    return BaseView().success_data(data=index, msg='图片分片提交失败')


@app.route('/api/switch_imgShard', methods=['POST'])
def switch_imgShard():
    """
    接受图片uuid,并转换为图片
    :return:
    """
    rules = {
        'uuid': {
            'required': True,
            'type': 'string'
        }
    }
    error_msg = {
        'uuid': {
            "required": '图片唯一id为必须',
            'type': '唯一id类型为字符串'
        }
    }
    error = BaseView().validate_input(rules=rules, error_msg=error_msg)
    if error is not True:
        return error
    uuid = request.form.get('uuid')
    data = ImgShard.get_data(uuid)
    base64_data = ''
    for i in data:
        base64_data = base64_data + i['imgString']
    user_img = base64_data.split(',')[1]
    img_data = base64.b64decode(user_img)
    real_path = '/uploads/' + Utils.unique_id() + '.jpg'
    path = os.getcwd() + real_path
    with open(path, 'wb') as f:
        f.write(img_data)
    return BaseView().success_data(data={'url': real_path}, msg='图片提交成功')
