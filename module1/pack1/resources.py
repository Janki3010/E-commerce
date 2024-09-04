from flask import request, session
from flask_restful import Resource
from flask_socketio import Namespace, emit

from module1 import mysql


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
            return {'message': 'success'}, 200
        else:
            return {'message': 'user not found'}, 404
        # if account:
        #     session['loggedin'] = True
        #     session['email'] = account[2]
        #     session['role'] = account[5]
        #
        #     return 'successful login'


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
        cur = mysql.connection.cursor()
        # products = cur.execute('select * from products')
        cur.callproc('fetch_product')
        products = cur.fetchall()

        # products_list = []
        # for product in products:
        #     # products_list.append({
        #     #     'name': product[1],
        #     #     'description': product[2],
        #     #     'price': product[3],
        #     #     'category': product[4],
        #     #     'image': product[5],
        #     #     'qty': product[6]
        #     # })
        #     products_list.append(list(product))

        return {'message': 'success', 'product': products}, 200


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
            response = "That’s great to hear! Anything exciting happening or anything you’re looking forward to?"
        elif message == "Nothing is going well":
            response = "I’m sorry to hear that things aren’t going well. Do you want to talk about what’s been going on?"
        elif message == "Thank you":
            response = "You’re welcome. If you feel like talking or if there’s anything I can do to help, just let me know."
        else:
            response = "Sorry, I don't understand that."
        emit('response', response)

    def on_disconnect(self):
        print('Clint disconnected')

