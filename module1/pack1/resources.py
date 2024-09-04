from flask import redirect, make_response, render_template, request
from flask_restful import Resource
import requests


class Register(Resource):
    def get(self):
        return make_response(render_template('register.html'))

    def post(self):
        data = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password'],
            "mobile": request.form['phone'],
            # "role": request.form['role'],
        }

        response = requests.post('http://127.0.0.1:6002/register', json=data)

        if response.status_code == 200:
            return redirect('http://127.0.0.1:6001/login')
        else:
            return make_response({"error": "Failed to insert data into the database"}, 500)


class Login(Resource):
    def get(self):
        return make_response(render_template('login.html'))

    def post(self):
        data = {
            "email": request.form['email'],
            "password": request.form['password']
        }

        if request.form['email'] == 'admin@gmail.com':
            return redirect('http://127.0.0.1:6001/admin')
        else:
            response = requests.post('http://127.0.0.1:6002/login', json=data)

            if response.status_code == 200:
                user_id = response.json().get('user_id')
                if user_id:
                    return redirect(f'http://127.0.0.1:6001/product_details?user_id={user_id}')
            else:
                return 'Error'


class Admin(Resource):
    def get(self):
        return make_response(render_template('admin_panel.html'))

    def post(self):
        data = {
            "id": request.form['product_id'],
            "name": request.form['product_name'],
            "description": request.form['product_description'],
            "price": request.form['product_price'],
            "category": request.form['product_categorie'],
            "image": request.form['filebutton'],
            "qty": request.form['available_quantity']
        }

        response = requests.post('http://127.0.0.1:6002/add_product', json=data)

        if response.status_code == 200:
            return 'Data added successfully'
        else:
            return 'Error'


class Products(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        response = requests.get('http://127.0.0.1:6002/products')
        if response.status_code == 200:
            data = response.json()['product']
            return make_response(render_template('product_details.html', products=data, user_id=user_id))
        else:
            return make_response('Error fetching product details', response.status_code)


class AddToCart(Resource):
    def post(self):
        data = {
            "user_id": request.form['user_id'],
            "product_id": request.form['product_id'],
            "product_price": request.form['product_price'],
            "quantity": request.form['quantity']
        }

        response = requests.post('http://127.0.0.1:6002/add_to_cart', json=data)

        if response.status_code == 200:
            return make_response('Product added to cart successfully', 200)
        else:
            return make_response('Error adding product to cart', response.status_code)


class ChatBot(Resource):
    def get(self):
        return make_response(render_template('chatbot.html'))
