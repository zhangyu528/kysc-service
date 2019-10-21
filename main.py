# -*- coding: utf-8 -*-  

from flask import Flask
from flask_restful import Api

from api.user import User
from api.login import Tel
from api.good import List, Category, Detail
from api.order import PrePay, DoPay

from api.auth import WXAuth

app = Flask(__name__)
api = Api(app)

api.add_resource(Tel, '/login/tel')
api.add_resource(User, '/user')
api.add_resource(List, '/good/list')
api.add_resource(Category, '/good/category')
api.add_resource(WXAuth, '/auth/wx')
api.add_resource(Detail, '/good/detail')
api.add_resource(PrePay, '/order/prePay')
api.add_resource(DoPay, '/order/doPay')

if __name__ == "__main__":
    app.run(debug=True, host='152.136.168.160', port=5000)
