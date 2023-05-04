import json

from flask import render_template, redirect, request, url_for, jsonify, flash, session, current_app
from shop import db, app
from shop.products.models import Brand, Category, Product
from shop.products.utils import get_all_brands, get_all_categories
from .models import GoodsInCarts, Carts

from flask_login import login_required, current_user, logout_user, login_user
from .utils import SessionCart, serialize_session_cart


@app.route('/cart', methods=['GET'])
def get_cart():
    if current_user.is_active:
        cart_id = session['cart_id']
        if len(session_cart := SessionCart.get()):
            for key, value in session_cart.items():
                if not (good_exist := GoodsInCarts.query.filter_by(cart_id=cart_id).filter_by(product_id=key).first()):
                    s = GoodsInCarts(cart_id=cart_id, product_id=key, quantity=value['quantity'])
                    db.session.add(s)
                else:
                    good_exist.quantity += value['quantity']
                db.session.commit()
            session.pop('ShoppingCart')
        goods_in_cart = GoodsInCarts.query.filter(
            GoodsInCarts.cart_id == cart_id).order_by(GoodsInCarts.id.desc()).all()
    else:
        session_cart = SessionCart()
        if len(sc := session_cart.get()):
            goods_in_cart = serialize_session_cart(session_cart=sc)
        else:
            goods_in_cart = ()
    return render_template('products/cart.html', products=goods_in_cart)


@app.route('/cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        if current_user.is_active:
            cart_id = session['cart_id']

            if good_exist := GoodsInCarts.query.filter_by(product_id=product_id).filter_by(cart_id=cart_id).first():
                if good_exist.quantity < good_exist.product.stock:
                    good_exist.quantity += 1
                    db.session.commit()
            else:
                new_good = GoodsInCarts(cart_id=cart_id, product_id=product_id, quantity=quantity)
                db.session.add(new_good)
                db.session.commit()
            print(f'Добавить в корзину: , {product_id=}, {quantity=}, {cart_id=}')
        else:
            # TODO SessionCart class
            session_cart = SessionCart()
            if product_id in (cur_cart := session_cart.get()):
                session_cart.update_quantity(product_id)
            else:
                new_good = {product_id: {'quantity': quantity, 'order': len(cur_cart)}}
                session_cart.add(new_good)
    return redirect(request.referrer)


@app.route('/cart_upd/<prod_id>/', methods=['GET'])
def sd(prod_id):
    val = request.args.get('v', 0, type=int)
    if current_user.is_active:
        cart_id = session['cart_id']
        p = GoodsInCarts.query.filter_by(product_id=prod_id).filter_by(cart_id=cart_id).first()
        p.quantity += val
        db.session.commit()
    else:
        s = SessionCart()
        s.update_quantity(prod_id, val)
    return redirect(url_for('get_cart'))


@app.route('/cart_del/<prod_id>', methods=['GET'])
def de(prod_id):
    if current_user.is_active:
        GoodsInCarts.query.filter_by(product_id=prod_id).delete()
        db.session.commit()
        goods_in_cart = GoodsInCarts.query.filter(
            GoodsInCarts.cart_id == session['cart_id']).order_by(GoodsInCarts.id.desc()).all()
    else:
        session_cart = SessionCart()
        session_cart.delete_item(prod_id)
        goods_in_cart = serialize_session_cart(session_cart.get())
    return jsonify({'output': render_template('test/cart_part.html', products=goods_in_cart)})


@app.route('/clear_cart', methods=['GET'])
def clear_cart():
    if current_user.is_active:
        GoodsInCarts.query.filter_by(cart_id=session['cart_id']).delete()
        db.session.commit()
    else:
        session['ShoppingCart'] = dict()

    return jsonify({'output': render_template('test/cart_part.html', products=())})
