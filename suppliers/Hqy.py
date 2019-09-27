# -*- coding: utf-8 -*-  
import requests

class Hqy:
    def login(self):
        phone = '123'
        password = '111111'
        payload = {
            'phone': phone,
            'password': password,
        }
        url = 'http://47.94.1.127:8010/sns/login'
        r = requests.post(url, json = payload)
        self.token = r.json()['result']['token']
        print(self.token)
        return

    def buy(self, good_id, good_cnt):