from module1 import api, socketio
from module1.pack1.resources import *

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(ForgotPassword, '/forgotPassword')
api.add_resource(ResetPassword, '/reset_password')
api.add_resource(AddProduct, '/add_product')
api.add_resource(ProductDetails, '/products')
api.add_resource(AddToCart, '/add_to_cart')
api.add_resource(cartProducts, '/cartPro')
api.add_resource(RemoveProducts, '/removeProduct')
api.add_resource(addCartProduct, '/addCartProduct')
api.add_resource(BuyProducts, '/buy_products')
api.add_resource(AddAddress, '/add_address')
api.add_resource(AllAddress, '/all_address')
api.add_resource(Logout, '/logout')
socketio.on_namespace(ChatBot('/chat'))
