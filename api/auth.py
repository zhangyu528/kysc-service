# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from itsdangerous import JSONWebSignatureSerializer
import time
from database.mongo import client
from bson import json_util
import json
import requests
from sns.Wx import Wx

from response import *

class WXAuth(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('code', type=str)
        self.parser.add_argument('encryptedData', type=str)
        self.parser.add_argument('iv', type=str)

        self.db = client["main"]
        super(WXAuth, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        code = args['code']
        #参数校验
        error = ApiError.check_param(code, str)
        if error is not None:
            return error

        encryptedData = args['encryptedData']
        error = ApiError.check_param(encryptedData, str)
        if error is not None:
            return error

        iv = args['iv']
        error = ApiError.check_param(iv, str)
        if error is not None:
            return error

        #解码wx openid
        appid = 'wxc4e842b5c56f443c'
        secret = '77b0864fffbd6b395fdaa4e28fb27c72'
        wx = Wx()
        data = wx.jscode2ses(code, appid, secret, encryptedData, iv)
        openId = data['openId']
        if openId is None:
            return ApiError.wx_jscode2ses_error
        #生成用户token
        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'openId': openId, 'time': time.time()})
        user_collection = self.db['user']
        user_collection.update(
            {'openId': openId},
            {'$set': {'token': token}},
            True
        )
        data = {'token':token}
        return ApiSuccess.success(data)
        
if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(WXAuth, '/auth/wx')
    app.run(debug=True)