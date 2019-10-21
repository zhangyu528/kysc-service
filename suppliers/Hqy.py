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
        Authorization = 'bearer ' + Hqy.token
        headers = {'Authorization': Authorization}
        r = requests.post(url, headers = headers, json = json)
        return r.json()

    def good_detail(self, act_gid):
        if act_gid is None:
            return {'message':'参数错误'}, 1001

        if Hqy.isLogin() is False:
            self.login()

        path = '/buymanager/goods/detail'
        url = Hqy.root + path
        json = {
            'act_gid': act_gid,
        }
        Authorization = 'bearer ' + Hqy.token
        headers = {'Authorization': Authorization}
        r = requests.post(url, headers = headers, json = json)
        return r.json()

    def buy(self, act_id, num):
        if act_id is None:
            return {'message':'参数错误'}, 1001
        if num is None:
            return {'message':'参数错误 '}, 1001
        
        if Hqy.isLogin() is False:
            self.login()

        json = {
            'act_gid': act_id,
            'num': num
        }
        path = '/buymanager/goods/buy'
        url = Hqy.root + path
        Authorization = 'bearer ' + self.token
        headers = {'Authorization': Authorization}
        r = requests.post(url, headers = headers, json = json)
        return r.json()

    def doPay(self, order_id):
        if order_id is None:
            return {'message':'参数错误'}, 1001

        if Hqy.isLogin() is False:
            self.login()

        json = {
            'order_id': order_id,
            'passwd': '123456'
        }
        path = '/buymanager/order/do_pay'
        url = Hqy.root + path
        Authorization = 'bearer ' + self.token
        headers = {'Authorization': Authorization}
        r = requests.post(url, headers = headers, json = json)
        print(r)
        return