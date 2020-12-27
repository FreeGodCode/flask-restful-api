# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:59 PM
from flask_restful import abort, reqparse, Resource

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '...'},
    'todo3': {'task': 'profit'},
}


def abort_if_todo_doesnt_exist(todo_id):
    """

    :param todo_id:
    :return:
    """
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parse = reqparse.RequestParser()
parse.add_argument('task')


class Todo(Resource):
    """操作单一资源(get/put/delete)"""

    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def put(self, todo_id):
        args = parse.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204


class TodoList(Resource):
    """操作(get/post)资源列表TodoList"""

    def get(self):
        return TODOS

    def post(self):
        args = parse.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
