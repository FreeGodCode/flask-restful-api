# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/22/20 4:59 PM
from threading import Lock

from flask import request, session
from flask_socketio import emit, join_room, leave_room

from app import socketio
from app.Models.VirtualCoin import VirtualCoin

thread = None
global thread_pool
thread_lock = Lock()
thread_pool = {}


def background_thread():
    """
    example of how to send server generated events to clients.
    增加一个线程后台程序,每次返回消息会增加一个线程,
    需要设置条件关闭,或者一直作为生产者
    :return:
    """
    count = 0
    while True:
        socketio.sleep()
        count += 1
        socketio.emit('my_request', {'data': 'server generated event', 'count': count}, namespace='/test')


@socketio.on('my_request_unthread', namespace='/test')
def test_connect_unthread(message):
    """
    不使用线程,后台开异步执行推送
    :param message:
    :return:
    """
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        emit('my_request', {'data': 'Connected', 'unthreadCount': count})


@socketio.on('my_request', namespace='/test')
def test_connect(message):
    """
    使用线程,后台异步执行推送
    :param message:
    :return:
    """
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
            emit('my_request', {'data': 'Connected', 'sid': request.sid})


@socketio.on('request_for_response', namespace='/test')
def give_response(message):
    """

    :param message:
    :return:
    """
    value = message.get('param')
    return value


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    """
    全局广播,不加只是单个页面通信
    :param message:
    :return:
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_broadcast_event', {'msg': message['data'], 'count': session['receive_count']}, broadcast=True)


@socketio.on('join', namespace='/ChatRoom')
def join(message):
    """
    聊天室模式,进入,离开,聊天
    客户端可以设置房间号,用来区分响应作用域
    :param message:
    :return:
    """
    name = message['name']
    room = message['room']
    join_room(room)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('join', {'room': 'welcome %s into the room %s' % (name, room), 'count': session['receive_count']}, room=room)


@socketio.on('leave', namespace='/ChatRoom')
def leave(message):
    """
    离开
    :param message:
    :return:
    """
    name = message['name']
    room = message['room']
    leave_room(room)
    emit('leave', {'room': '%s leave up room %s' % (name, room)}, room=room)


@socketio.on('chat', namespace='/ChatRoom')
def chat(message):
    """
    聊天
    :param message:
    :return:
    """
    name = message['name']
    room = message['room']
    msg = message['msg']
    emit('chat', {'msg': msg, 'name': name}, room=room)


def background_virtual_thread(sid):
    while thread_pool['sid']['status']:
        socketio.sleep(1)
        try:
            data = VirtualCoin().get_ws_content(thread_pool[sid]['coinName'])
            socketio.emit('Virtual', {'data': data}, namespace='/VirtualCoin', room=thread_pool[sid]['sid'])
        except:
            pass
    del thread_pool[sid]


@socketio.on('virtual', namespace='VirtualCoin')
def virtual(message):
    """
    实时推送虚拟货币详情
    :param message:
    :return:
    """
    if 'leave' in message:
        thread_pool[request.sid]['status'] = False
    elif request.sid in thread_pool:
        thread_pool[request.sid]['coinName'] = message['coinName']
    else:
        thread_pool[request.sid] = {
            'status': True,
            'thread': '',
            'sid': request.sid,
            'coinName': message['coinName']
        }
        thread_pool[request.sid]['thread'] = socketio.start_background_task(background_virtual_thread, request.sid)


@socketio.on('connect', namespace='/test')
def connect():
    """
    连接事件
    :return:
    """
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def disconnect():
    """
    断开事件
    :return:
    """
    thread_pool[request.sid]['status'] = False


@socketio.on('disconnect', namespace='VirtualCoin')
def virtual_coin_disconnect():
    """
    断开事件
    :return:
    """
    thread_pool[request.sid]['status'] = False
