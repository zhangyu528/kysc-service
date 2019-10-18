# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from database.mongo import client
from bson import json_util
import json
from suppliers.Hqy import Hqy
from sns.Wx import Wx
from response import *

class PrePay(Resource):
    def __init__(self):
        self.db = client["main"]
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('act_id', type=str)
        self.parser.add_argument('num', type=str)
        self.parser.add_argument('Authorization', type=str, location='headers')
        super(PrePay, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        act_id = args['act_id']
        num = args['num']
        token = args['Authorization']

        error = ApiError.check_param(act_id, str)
        if error is not None:
            return error
        error = ApiError.check_param(num, str)
        if error is not None:
            return error
        error = ApiError.check_param(token, str)
        if error is not None:
            return ApiError.authorization_error

        #调用供应商提供接口购买接口
        hqy = Hqy()
        result = hqy.buy(act_id, num)
        data = result['result']
        order_id = data['order_id']

        #查找openId
        user_collection = self.db['user']
        result = user_collection.find_one({'token':token}, {'openId': 1, '_id': 0})
        data = json.loads(json_util.dumps(result))
        openId = data['openId']
        #调用微信统一支付订单
        wx = Wx()
        #二次签名返回给前端
        print(result)
        return {'message':'成功', 'data':data}, 200

# 支付成功回调url
class DoPay(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=str)
        super(DoPay, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        order_id = args['order_id']

        #调用供应商提供接口
        hqy = Hqy()
        result = hqy.doPay(order_id)
        data = result['result']['goods_info']
        print(data)
        return {'message':'成功', 'data':data}, 200

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PrePay, 'order/prePay')
    api.add_resource(DoPay, '/order/doPay')
    app.run(debug=True)