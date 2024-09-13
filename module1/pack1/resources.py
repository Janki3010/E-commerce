from flask import request, session, jsonify
from flask_restful import Resource
from flask_socketio import Namespace, emit
import json
from module1 import mysql, redis_client


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


# access_token = ''


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
            # global access_token
            user_id = account[0]
            # access_token = create_access_token(identity=user_id)
            session['loggedin'] = True
            session['id'] = account[0]
            redis_client.set('user_id', user_id)
            # session['email'] = account[2]
            # session['username'] = account[1]
            return {'message': 'success', 'user_id': user_id}, 200
            # return {'message': 'success', 'access_token': access_token, 'user_id': user_id}, 200
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
        cur = mysql.connection.cursor()
        # products = cur.execute('select * from products')
        cur.callproc('fetch_product')
        products = cur.fetchall()

        return {'message': 'success', 'product': products}, 200


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


class cartProducts(Resource):
    def get(self):
        user_id = redis_client.get('user_id')
        if user_id is None:
            return {'message': 'User ID not found in Redis'}, 404

        try:
            user_id = int(user_id)
            cur = mysql.connection.cursor()
            cur.callproc('cart_products', [user_id])
            products = cur.fetchall()
            cur.close()

            if not products:
                return {'message': 'No products found'}, 404
            # products = list(products)
            return {'message': 'success', 'products': list(products)}

        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 500


class RemoveProducts(Resource):
    def post(self):
        data = request.json
        cart_id = data.get('cart_id')
        qty = data.get('qty')

        if cart_id and qty:
            try:
                cur = mysql.connection.cursor()
                cur.callproc('updateCart', [int(cart_id), int(qty)])
                mysql.connection.commit()
                cur.close()
                return {"message": "Product removed from the cart successfully"}, 200
            except Exception as e:
                print(f"Error: {e}")
                return {"message": "Failed to remove product"}, 500
        return {"message": "Invalid input"}, 400


class addCartProduct(Resource):
    def post(self):
        data = request.json
        cart_id = data.get('cart_id')
        qty = data.get('qty')

        if cart_id and qty:
            try:
                cur = mysql.connection.cursor()
                cur.callproc('addProduct', [int(cart_id), int(qty)])
                mysql.connection.commit()
                cur.close()
                return {"message": "Product added to the cart successfully"}, 200
            except Exception as e:
                print(f"Error: {e}")
                return {"message": "Failed to add product"}, 500
        return {"message": "Invalid input"}, 400


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
        elif message == "Which types of products available here?":
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
