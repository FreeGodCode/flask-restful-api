# -*- coding: utf-8  -*-
# @Author: ty
# @File name: BaseModel.py
# @IDE: PyCharm
# @Create time: 12/22/20 5:04 PM
import json

import requests

from app.Models.BaseModel import BaseModel


class VirtualCoin(BaseModel):
    """虚拟货币模型类"""

    def get_ws_content(self, CoinName):
        url = ''
        data = '{"Command": 2, "Body": {"Coin": "%s", "Currency": "USD", "Base": "CNY"}}' % (CoinName)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Content-Length': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '',
            'Host': '',
            'Origin': '',
            'Referer': '',
            'User-Agent': '',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            datas = json.loads(response.text)
            return datas
        except:
            return {'Body': {'Items': []}}
