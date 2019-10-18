# -*- coding: utf-8 -*-  
import requests
import string
import random
import hashlib

try:
    from flask import request
except Exception:
    request = None

from aes.WXBizDataCrypt import WXBizDataCrypt


class Wx:
    def jscode2ses(self, code, appid, secret, encryptedData, iv):
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {
            'appid': appid,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        r = requests.get(url, params = payload)
        sessionKey = r.json()['session_key']
        pc = WXBizDataCrypt(appid, sessionKey)
        data = pc.decrypt(encryptedData, iv)
        return data

class WxPayError:
    appid_error = Exception('缺少appid必填参数')
    mch_id_error = Exception('缺少mch_id必填参数')
    openid_error = Exception('缺少openid必填参数')
    out_trade_no_error = Exception('缺少out_trade_no必填参数')
    total_fee_error = Exception('缺少total_fee必填参数')

class WxPay:
    HOST = "https://api.mch.weixin.qq.com"
    #注：key为商户平台设置的密钥key
    mch_key = "gegewewefwfwfewgwgwegf23424244422"

    @property
    def nonce_str(self):
        char = string.ascii_letters + string.digits
        return "".join(random.choice(char) for _ in range(32))

    @property
    def remote_addr(self):
        if request is not None:
            return request.remote_addr
        return ""

    def sign(self, raw):
        raw = [(k, str(raw[k]) if isinstance(raw[k], int) else raw[k])
        for k in sorted(raw.keys())]
        s = "&".join("=".join(kv) for kv in raw if kv[1])
        s += "&key={0}".format(WxPay.mch_key)
        return hashlib.md5(s.encode("utf-8")).hexdigest().upper()

    def to_xml(self, raw):
        s = ""
        for k, v in raw.items():
            s += "<{0}>{1}</{0}>".format(k, v)
        s = "<xml>{0}</xml>".format(s)
        return s.encode("utf-8")
    
    def unified_order(self, **data):
        url = WxPay.HOST + '/pay/unifiedorder'

        #必填参数
        if "appid" not in data:
            raise WxPayError.appid_error

        if "mch_id" not in data:
            raise WxPayError.mch_id_error

        if "openid" not in data:
            raise WxPayError.openid_error

        if "out_trade_no" not in data:
            raise WxPayError.out_trade_no_error

        if "total_fee" not in data:
            raise WxPayError.total_fee_error

        data["body"] = 'kysc-卡券'
        data["trade_type"] = 'JSAPI'
        data["notify_url"] = 'http://localhost/order/doPay'
        data["nonce_str"] = self.nonce_str
        data["sign"] = self.sign(data)

        resp = requests.post(url, data = data)
        print(resp)
        pass