from flask import session
from shop.products.models import Product
from .models import GoodsInCarts


class SessionCart:
    @staticmethod
    def get():
        if session_cart := session.get('ShoppingCart', False):
            return session_cart
        else:
            session['ShoppingCart'] = dict()
            return session['ShoppingCart']

    def add(self, new_item):
        session['ShoppingCart'] = {**new_item, **self.get()}

    @staticmethod
    def update_quantity(product_id, val=1):
        cur_q = session['ShoppingCart'][product_id]['quantity']

        if (p := Product.query.filter_by(id=product_id).first().stock) > cur_q or p > cur_q + val:
            session.modified = True
            session['ShoppingCart'][product_id]['quantity'] += val

    def delete_item(self, product_id):
        session_cart = self.get()
        session.modified = True
        session_cart.pop(product_id)


class InSessionCart:
    def __init__(self, prod, quant):
        self.product = prod
        self.quantity = quant


def serialize_session_cart(session_cart):
    p_ids = []
    quant = []
    order = []
    for key, value in session_cart.items():
        p_ids.append(key)
        print(key, value)
        quant.append(value['quantity'])
        order.append(value['order'])
    res = []
    sc = zip(p_ids, quant, order)
    sort_sc = sorted(sc, key=lambda x: x[2])
    for el in sort_sc:
        product = Product.query.filter_by(id=el[0]).first()
        res.append(InSessionCart(product, el[1]))
    return res
