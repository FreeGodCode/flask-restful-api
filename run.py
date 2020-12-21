# -*- coding: utf-8  -*-
# @Author: ty
# @File name: run.py 
# @IDE: PyCharm
# @Create time: 12/21/20 5:50 PM
from flask_cors import CORS

from app import create_app


app = create_app()






CORS(app, suports_credentials=True)
if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.1', port=5000)
