# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from itsdangerous import JSONWebSignatureSerializer
import time
from database.mongo import client
from bson import json_util
import json

class Tel(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('code', type=str)
        self.db = client["main"]
        super(Tel, self).__init__()
        
    def post(self):
        args = self.parser.parse_args()
        phone = args['phone']
        code = args['code']

        if phone is None or code is None:
            return {'message':'参数错误'}, 1001
        if len(phone) == 0 or len(code) == 0:
            return {'message':'参数错误'}, 1001

        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'phone': phone, 'time':time.time()})
        user_collection = self.db['user']
        user_collection.update(
            {'tel': phone},
            {'$set': {'token': token}},
            True
        )
        return {'message':'成功', 'token':token}, 200

class UserReg(Resource):
    def __init__(self):
        super(UserReg, self).__init__()
    
    def post(self):
        args = self.prase.parse_args()
        username = args['username']
        password = args['password']

        if username is None or password is None:
            return {'message':'参数错误'}, 1001
        if len(username) == 0 or len(password) == 0:
            return {'message':'参数错误'}, 1001
        
        user_collection = self.db['user']
        result = user_collection.find(
            {
                'username': username
            }
        )
        if result is None:
            return {'message':'用户已经注册'}, 2001
        
        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'username': username, 'time':time.time()})
        user_collection.insert({
            {
                'username': username,
                'password': password,
                'token': token
            }
        })
        return {'message':'成功', 'token':token}, 200

class UserName(Resource):
    def __init__(self):
        self.prase = reqparse.RequestParser()
        self.prase.add_argument('username', type=str)
        self.prase.add_argument('password', type=str)
        super(UserName, self).__init__()

    def post(self):
        args = self.prase.parse_args()
        username = args['username']
        password = args['password']

        if username is None or password is None:
            return {'message':'参数错误'}, 1001
        if len(username) == 0 or len(password) == 0:
            return {'message':'参数错误'}, 1001

        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'username': username, 'time':time.time()})
        user_collection = self.db['user']
        user_collection.update(
            {'username': username},
            {'$set': {'password': password,
                      'token': token
                     }
            },
            False
        )
        return {'message':'成功', 'token':token}, 200


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Tel, '/login/tel')
    api.add_resource(UserReg, '/reg/user')
    api.add_resource(UserName, '/login/username')
    app.run(debug=True)