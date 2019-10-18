# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from itsdangerous import JSONWebSignatureSerializer
import time
from database.mongo import client
from bson import json_util
import json

from response import *

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
        error = ApiError.check_param(phone, str)
        if error is not None:
            return error
            
        code = args['code']
        error = ApiError.check_param(code, str)
        if error is not None:
            return error

        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'phone': phone, 'time':time.time()})
        user_collection = self.db['user']
        user_collection.update(
            {'tel': phone},
            {'$set': {'token': token}},
            True
        )
        data = {'token':token}
        return ApiSuccess.success(data)

class UserReg(Resource):
    def __init__(self):
        super(UserReg, self).__init__()
    
    def post(self):
        args = self.prase.parse_args()
        username = args['username']
        error = ApiError.check_param(username, str)
        if error is not None:
            return error
        password = args['password']
        error = ApiError.check_param(password, str)
        if error is not None:
            return error
        
        user_collection = self.db['user']
        result = user_collection.find(
            {
                'username': username
            }
        )
        if result is not None:
            return ApiError.user_exist_error
        
        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'username': username, 'time':time.time()})
        user_collection.insert({
            {
                'username': username,
                'password': password,
                'token': token
            }
        })
        data = {'token':token}
        return ApiSuccess.success(data)

class UserName(Resource):
    def __init__(self):
        self.prase = reqparse.RequestParser()
        self.prase.add_argument('username', type=str)
        self.prase.add_argument('password', type=str)
        super(UserName, self).__init__()

    def post(self):
        args = self.prase.parse_args()
        username = args['username']
        error = ApiError.check_param(username, str)
        if error is not None:
            return error
        password = args['password']
        error = ApiError.check_param(password, str)
        if error is not None:
            return error

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
        data = {'token':token}
        return ApiSuccess.success(data)


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Tel, '/login/tel')
    api.add_resource(UserReg, '/reg/user')
    api.add_resource(UserName, '/login/username')
    app.run(debug=True)