from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Product, Brand, Category
from flask_login import login_required


@app.route('/admin')
@login_required
def admin():
    products: Product = Product.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)


@app.route('/admin/brands')
def brands():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('admin_login'))
    brands = Brand.query.order_by(Brand.id.asc()).all()
    return render_template('admin/brands.html', title='Brand page', brands=brands)


@app.route('/admin/categories')
def categories():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('admin_login'))
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/brands.html', title='Category page', categories=categories)


@app.route('/admin/reg', methods=['GET', 'POST'])
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'Welcome {form.name.data}! Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('admin_login'), code=302)
    return render_template('admin/register.html', form=form, title='Register user')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {user.name}. You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password, please try again', 'danger')
    return render_template('admin/login.html', form=form, title='Login Page')


@app.route('/admin/logout')
def admin_logout():
    if 'email' in session:
        session.clear()
        print(session)
    return redirect(url_for('admin_login'))
