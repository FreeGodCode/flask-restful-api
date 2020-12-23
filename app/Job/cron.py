# -*- coding: utf-8  -*-
# @Author: ty
# @File name: cron.py 
# @IDE: PyCharm
# @Create time: 12/23/20 10:50 PM
import time

from app import scheduler


# 定时任务,触发类型为cron类型,每隔5秒,循环执行
@scheduler.scheduled_job('cron', second=5)
def cron_job():
    print('<cron_job>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
