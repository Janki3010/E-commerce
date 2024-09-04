from flask import request, session
from flask_restful import Resource
from flask_socketio import Namespace, emit

from BackendModule import mysql


class Register(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        mobile = data.get('mobile')
        # role = data.get('role')

        cur = mysql.connection.cursor()
        # cur.callproc('add_user', (username, email, password, mobile, role))
        cur.callproc('add_user_data', (username, email, password, mobile))
        mysql.connection.commit()
        cur.close()

        return {"message": "Data inserted successfully"}, 200


class Login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        cur = mysql.connection.cursor()
        cur.execute('select * from users where email = %s and password = %s', (email, password))
        account = cur.fetchone()
        cur.close()
        if account:
            user_id = account[0]
            session['loggedin'] = True
            session['id'] = account[0]
            # session['email'] = account[2]
            # session['username'] = account[1]
            return {'message': 'success', 'user_id': user_id}, 200
        else:
            return {'message': 'user not found'}, 404


class AddProduct(Resource):
    def post(self):
        data = request.json
        id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')
        image = data.get('image')
        qty = data.get('qty')

        cur = mysql.connection.cursor()
        cur.callproc('add_product', (id, name, description, price, category, image, qty))
        mysql.connection.commit()
        cur.close()

        return {"message": "Data inserted successfully"}, 200


class ProductDetails(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        cur = mysql.connection.cursor()
        # products = cur.execute('select * from products')
        cur.callproc('fetch_product')
        products = cur.fetchall()

        return {'message': 'success', 'product': products, 'user_id': user_id}, 200


class AddToCart(Resource):
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        product_price = data.get('product_price')
        quantity = data.get('quantity')

        if not user_id or not product_id or not quantity:
            return {"message": "Missing required fields"}, 400

        cur = mysql.connection.cursor()
        cur.callproc('add_to_cart', (user_id, product_id, quantity, product_price))
        mysql.connection.commit()
        cur.close()

        # emit('cart_update', {'product_id': product_id, 'quantity': quantity}, room=user_id)

        return {"message": "Product added to cart successfully"}, 200


class ChatBot(Namespace):
    def on_connect(self):
        print('Clint connected')

    def on_message(self, message):
        print('Received message: ' + message)
        if message == 'Hii':
            response = 'Hiii! How can I help you?'
        elif message == 'How are you?':
            response = "I’m doing great, thanks for asking! I’m here and ready to help with whatever you need."
        elif message == 'Everything is going well':
            response = "That’s great to hear!"
        elif message == "Which types of products do u have?":
            response = '1.Beauty & Personal Care 2.Arts 3.Electronic 4.Home & Kitchen 5.Toys & Games'
        elif message == "Beauty & Personal Care" or message == "Arts" or message == "Electronic" or message == "Home & Kitchen" or message == "Toys & Games":
            response = 'Yes this product is available'
        elif message == "Nothing is going well":
            response = "I’m sorry to hear that things aren’t going well. Do you want to talk about what’s been going on?"
        elif message == "Thank you":
            response = "You’re welcome."
        else:
            response = "Sorry, I don't understand that."
        emit('response', response)

    def on_disconnect(self):
        print('Clint disconnected')


class Logout(Resource):
    def get(self):
        session.pop('loggedin', None)
        session.pop('id', None)

        return {"message": "Logged out successfully"}, 200
