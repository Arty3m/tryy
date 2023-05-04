import os
import secrets

from flask import render_template, redirect, request, url_for, flash, session, current_app
from shop import db, app, search, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import secure_filename
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import CustomerUser
from shop.carts.models import Carts


@app.route('/register', methods=['POST', 'GET'])
def register():
    # form = CustomerRegisterForm(request.form)
    form = CustomerRegisterForm()
    print('DO validate')
    print(form.data)
    if form.validate_on_submit():
        # print(form.profile.data)
        # # TODO fix adding photo
        profile_tmp = 'profile.jpg'
        hash_password = bcrypt.generate_password_hash(form.password.data)
        customer_user = CustomerUser(name=form.name.data, username=form.username.data, email=form.email.data,
                                     password=hash_password, city=form.city, profile=profile_tmp)
        db.session.add(customer_user)
        db.session.commit()
        new_cart = Carts(user_id=customer_user.id)
        db.session.add(new_cart)
        db.session.commit()
        flash(f'Добро пожаловать, {form.name.data}. Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login_view'))
    return render_template('customers/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = CustomerLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = CustomerUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user)
            session['email'] = form.email.data
            flash('You are logged in now', 'success')
            next_url = request.args.get('next')
            # TODO ADD a check func
            # if not is_safe_url(next):
            #     return flask.abort(400)
            session['cart_id'] = Carts.query.filter_by(user_id=user.id).first().id
            return redirect(next_url or url_for('home'))
        else:
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('login_view'))
    return render_template('customers/login.html', form=form, title='Login Page')


@app.route('/logout')
def logout():
    if current_user.is_active:
        logout_user()
    session.clear()
    return redirect(url_for('home'))


@app.route('/test', methods=["POST", "GET"])
def test():
    if current_user.is_active:
        print('Текущий юзер:', current_user.id, current_user.username)
    reg_form = CustomerRegisterForm()
    log_form = CustomerLoginForm()
    if log_form.validate_on_submit():
        print('popalo')
        print(log_form.data)
    # print('==>',reg_form.data)
    if reg_form.validate_on_submit():
        print('SUDA')
        print(reg_form.data)
        us = CustomerUser(name='test', username=reg_form.username.data, password=hash(reg_form.password.data),
                          email=reg_form.email.data, city='msk', profile="profile.png")
        print(us)

    return render_template('test/index.html', register=reg_form, login=log_form)
