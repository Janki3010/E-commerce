import os
import random

from flask import redirect, make_response, render_template, request, url_for, flash, session
from flask_mail import Message
from flask_restful import Resource
import requests
from module1 import app, RECAPTCHA_SECRET_KEY
from module1 import mail


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
        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()

        if not result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.')
            return redirect('/login')  # Redirect to the login page
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


class ForgotPassword(Resource):
    def get(self):
        return make_response(render_template('forgot_password.html'))

    def post(self):
        email = request.form['email']
        data = {'email': email}
        response = requests.post('http://127.0.0.1:6002/forgotPassword', json=data)

        if response.status_code != 200:
            flash('Email does not exist.', 'danger')
            return redirect(url_for('forgot_password'))

        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP

        msg = Message('Your OTP for Password Reset', recipients=[email])
        msg.body = f'Your OTP is {otp}. Please use it to reset your password.'

        try:
            mail.send(msg)
            flash('Check your email for the OTP!', 'info')
        except Exception as e:
            flash('Failed to send email. Please try again later.', 'danger')
            app.logger.error(f'Error sending email: {str(e)}')

        session['otp'] = otp
        return redirect('http://127.0.0.1:6001/validate_otp')


class ValidateOTP(Resource):
    def get(self):
        return make_response(render_template('validate_otp.html'))

    def post(self):
        entered_otp = request.form['otp']

        if 'otp' in session and session['otp'] == int(entered_otp):
            return redirect('http://127.0.0.1:6001/reset_password')
        else:
            flash('Invalid or expired OTP.', 'danger')
            return redirect('http://127.0.0.1:6001/forgot_password')


class ResetPassword(Resource):
    def get(self):
        return make_response(render_template('reset_password.html'))  # Render reset password form

    def post(self):
        new_password = request.form['password']

        data = {'new_password': new_password}
        response = requests.post('http://127.0.0.1:6002/reset_password', json=data)

        if response.status_code == 200:
            flash('Your password has been updated!', 'success')
            return redirect(f'http://127.0.0.1:6001/login')  # Ensure 'login' is defined in your routes
        else:
            flash('Failed to update password.', 'danger')
            return redirect(url_for('reset_password'))


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
        user_id = request.form['user_id']

        data = {
            "user_id": request.form['user_id'],
            "product_id": request.form['product_id'],
            "product_price": request.form['product_price'],
            "quantity": request.form['quantity']
        }

        response = requests.post('http://127.0.0.1:6002/add_to_cart', json=data)

        if response.status_code == 200:
            if user_id:
                return redirect(f'http://127.0.0.1:6001/product_details?user_id={user_id}')
            # return make_response('Product added to cart successfully', 200)
        else:
            return make_response('Error adding product to cart', response.status_code)


class BuyProducts(Resource):
    def post(self):
        response = requests.get('http://127.0.0.1:6002/buy_products')

        if response.status_code == 200:
            data = response.json()['products']
            total = response.json()['total_price']
            return make_response(render_template('buy_products.html', products=data, total=total))
        else:
            return make_response('Error at time buy the product', response.status_code)


class ProcessPayment(Resource):
    def get(self):
        return make_response(render_template('payment.html'))


class AllAddress(Resource):
    def post(self):
        response = requests.get('http://127.0.0.1:6002/all_address')

        if response.status_code == 200:
            address = response.json()['user_address']
            return make_response(render_template('payment.html', all_address=address))
        else:
            return make_response('Error at time to fetch all the addresses', response.status_code)


class AddAddress(Resource):
    def get(self):
        return make_response(render_template('add_address.html'))

    def post(self):
        data = {
            "name": request.form['name'],
            "street-address": request.form['street-address'],
            "postal-code": request.form['postal-code'],
            "city": request.form['city'],
            "country": request.form['country']
        }

        response = requests.post('http://127.0.0.1:6002/add_address', json=data)

        if response.status_code == 200:
            return redirect('http://127.0.0.1:6001/payment')
        else:
            return make_response({"error": "Failed to insert data into the database"}, 500)


class ChatBot(Resource):
    def get(self):
        return make_response(render_template('chatbot.html'))


class CartProducts(Resource):
    def get(self):
        response = requests.get('http://127.0.0.1:6002/cartPro')
        if response.status_code == 200:
            data = response.json()['products']
            return make_response(render_template('cartProducts.html', products=data))
        else:
            return make_response('Error fetching product details', response.status_code)


class SuccessPayment(Resource):
    def get(self):
        return make_response(render_template('successPayment.html'))


# class RemoveProduct(Resource):
#     def post(self):
#         data = {
#             "cart_id": request.form['cart_id'],
#             "qty": request.form['qty']
#         }
#         response = requests.post('http://127.0.0.1:6002/removeProduct', json=data)
#         if response.status_code == 200:
#            return {'message': 'success'}, 200
#         return {'message': 'Faild'}, 404


class Logout(Resource):
    def get(self):
        response = requests.get('http://127.0.0.1:6002/logout')
        if response.status_code == 200:
            return redirect('http://127.0.0.1:6001/login')
