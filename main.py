# -*- coding: utf-8 -*-  

from flask import Flask
from flask_restful import Api

from api.user import User
from api.login import Tel
from api.good import List
from api.good import Category
from api.auth import WXAuth
from suppliers.Hqy import Hqy

app = Flask(__name__)
api = Api(app)

api.add_resource(Tel, '/login/tel')
api.add_resource(User, '/user')
api.add_resource(List, '/good/list')
api.add_resource(Category, '/good/category')
api.add_resource(WXAuth, '/auth/wx')

hqy = Hqy()
hqy.login()

if __name__ == "__main__":
    app.run(debug=True)
