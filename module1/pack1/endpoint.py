from module1 import api
from module1.pack1.resources import *

api.add_resource(Register, '/')
api.add_resource(Login, '/login')
api.add_resource(Admin, '/admin')
api.add_resource(Products, '/product_details')
api.add_resource(AddToCart, '/add_to_cart')
api.add_resource(CartProducts, '/show_cart')
# api.add_resource(RemoveProduct, '/remove')
api.add_resource(BuyProducts, '/Buy_Products')
api.add_resource(AddAddress, '/add_address')
api.add_resource(ProcessPayment, '/payment')
api.add_resource(AllAddress, '/all_address')
api.add_resource(ChatBot, '/chatbot')
api.add_resource(Logout, '/logout')
