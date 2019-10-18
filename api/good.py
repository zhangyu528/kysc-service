# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from database.mongo import client
from bson import json_util
import json

from suppliers.Hqy import Hqy
from response import *

class Detail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('act_id', type=str)
        super(Detail, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        act_id = args['act_id']

        #参数校验
        error = ApiError.check_param(act_id, str)
        if error is not None:
            return error
        
        #调用供应商提供接口获取商品list
        hqy = Hqy()
        resp = hqy.good_detail(act_id)
        if resp['status'] == 'y':
            data = resp['result']['goods_info']
            return ApiSuccess.success(data)
        else:
            return ApiError.suppliers_service_errror

class Category(Resource):
    def __init__(self):
        self.db = client["main"]
        super(Category, self).__init__()
    
    def get(self):
        category_collection = self.db['category']
        category = category_collection.find({})
        data = json.loads(json_util.dumps(category))
        return ApiSuccess.success(data)

class List(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cat_id', type=str)
        self.db = client["main"]
        super(List, self).__init__()
    
    def post(self):
        args = self.parser.parse_args()
        cat_id = args['cat_id']
        #参数校验
        error = ApiError.check_param(cat_id, str)
        if error is not None:
            return error

        #调用供应商提供接口获取商品list
        hqy = Hqy()
        resp = hqy.goods_list(cat_id)
        if resp['status'] == 'y':
            data = resp['result']['goods']
            return ApiSuccess.success(data)
        else:
            return ApiError.suppliers_service_errror


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(List, '/good/list')
    api.add_resource(Category, '/good/category')
    api.add_resource(Detail, '/good/detail')
    app.run(debug=True)