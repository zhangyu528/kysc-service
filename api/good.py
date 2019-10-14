# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from database.mongo import client
from bson import json_util
import json
from suppliers.Hqy import Hqy

class Detail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('act_id', type=str)
        super(Detail, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        act_id = args['act_id']
        if act_id is None:
            return {'message':'参数错误'}, 1001

        #调用供应商提供接口获取商品list
        hqy = Hqy()
        result = hqy.good_detail(act_id)
        data = result['result']['goods_info']
        return {'message':'成功', 'data':data}, 200

class Category(Resource):
    def __init__(self):
        self.db = client["main"]
        super(Category, self).__init__()
    
    def get(self):
        category_collection = self.db['category']
        category = category_collection.find({})
        data = json.loads(json_util.dumps(category))
        return {'message':'成功', 'data':data}, 200

class List(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cat_id', type=str)
        self.db = client["main"]
        super(List, self).__init__()
    
    def post(self):
        args = self.parser.parse_args()
        cat_id = args['cat_id']

        if cat_id is None:
            return {'message':'参数错误'}, 1001
        if len(cat_id) == 0:
            return {'message':'参数错误'}, 1001
        
        # category_collection = self.db['category']
        # goods_id = category_collection.find_one({'cat_id':cat_id}, {'goods': 1, '_id': 0})
        # ids = json.loads(json_util.dumps(goods_id))['goods']
        # good_collection = self.db['good']
        # data = json.loads(json_util.dumps(good_collection.find({'id': { '$in': ids }}, {'_id':0})))

        #调用供应商提供接口获取商品list
        hqy = Hqy()
        result = hqy.goods_list(cat_id)
        data = result['result']['goods']
        print(data)
        return {'message':'成功', 'data':data}, 200


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(List, '/good/list')
    api.add_resource(Category, '/good/category')
    api.add_resource(Detail, '/good/detail')
    app.run(debug=True)