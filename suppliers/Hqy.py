# -*- coding: utf-8 -*-  
import requests

class Hqy:
    root = 'http://47.94.1.127:8010'
    token = ''

    def __init__(self):
        return

    @staticmethod   
    def isLogin():
        if Hqy.token != '':
            return True
        return False
    
    def login(self):
        phone = '123'
        password = '111111'
        json = {
            'phone': phone,
            'password': password,
        }
        path = "/sns/login"
        url = Hqy.root + path
        r = requests.post(url, json = json)
        Hqy.token = r.json()['result']['token']
        return



    def goods_list(self, cat_id):

        if cat_id is None:
            return {'message':'参数错误'}, 1001

        if Hqy.isLogin() is False:
            self.login()

        path = '/buymanager/goods/list'
        url = Hqy.root + path
        json = {
            'cat_id': cat_id,
        }
        Authorization = 'bearer ' + self.token
        headers = {'Authorization': Authorization}
        r = requests.post(url, headers = headers, json = json)
        return r.json()

    def buy(self, good_id, good_cnt):
        json = {
            'act_gid': good_id,
            'num': good_cnt
        }
        path = '/buymanager/goods/buy'
        url = Hqy.root + path
        r = requests.post(url, json = json)
        print(r)
        return