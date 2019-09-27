# -*- coding: utf-8 -*-  
from flask import Flask
from flask_restful import Api, Resource, reqparse
from itsdangerous import JSONWebSignatureSerializer
import time
from database.mongo import client
from bson import json_util
import json
import requests
from aes.WXBizDataCrypt import WXBizDataCrypt

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
        if code is None or code is None:
            return {'message':'参数错误'}, 1001

        encryptedData = args['encryptedData']
        if encryptedData is None or code is None:
            return {'message':'参数错误'}, 1001

        iv = args['iv']
        if iv is None or code is None:
            return {'message':'参数错误'}, 1001

        appid = 'wxc4e842b5c56f443c'
        secret = '77b0864fffbd6b395fdaa4e28fb27c72'
        payload = {
            'appid': appid,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        r = requests.get(url, params = payload)
        sessionKey = r.json()['session_key']

        pc = WXBizDataCrypt(appid, sessionKey)

        data = pc.decrypt(encryptedData, iv)

        openId = data['openId']
        token = JSONWebSignatureSerializer('secret-key')
        token = token.dumps({'openId': openId, 'time':time.time()})
        user_collection = self.db['user']
        user_collection.update(
            {'openId': openId},
            {'$set': {'token': token}},
            True
        )
        return {'message':'成功', 'token':'token'}, 200
        
if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(WXAuth, '/auth/wx')
    app.run(debug=True)