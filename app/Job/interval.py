# -*- coding: utf-8  -*-
# @Author: ty
# @File name: interval.py 
# @IDE: PyCharm
# @Create time: 12/23/20 10:54 PM
import time

from app import scheduler

# 定时任务,使用interval触发类型,并使用装饰器实现,循环执行,每隔5秒钟执行一次
@scheduler.scheduled_job('interval', second=5)
def interval_job():
    print('<interval_job>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))