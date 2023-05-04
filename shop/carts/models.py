from shop import db, login_manager
from datetime import datetime


# TODO add delete on cascade on user_id
class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=False)


class GoodsInCarts(db.Model):
    __tablename__ = 'goods_in_cart'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    # product_id = db.Column(db.Integer, nullable=False)
    # or
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('products', lazy=True))

    quantity = db.Column(db.Integer, nullable=False)

