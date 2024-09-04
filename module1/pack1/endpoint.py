from module1 import api
from module1.pack1.resources import *

api.add_resource(Register, '/')
api.add_resource(Login, '/login')
api.add_resource(Admin, '/admin')
api.add_resource(Products, '/product_details')
api.add_resource(AddToCart, '/add_to_cart')
api.add_resource(ChatBot, '/chatbot')
