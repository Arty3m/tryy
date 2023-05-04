from datetime import datetime
from shop import db
from slugify import slugify


class Product(db.Model):
    __tablename__: str = 'product'
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))

    def __repr__(self):
        return '<Product %r>' % self.name

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'description': self.description}


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    slug = db.Column(db.String(50), index=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Brand %r>' % self.name
    # def __str__(self):
    #     return self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


class CharacteristicType(db.Model):
    __tablename__ = 'characteristic_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Characteristic(db.Model):
    __tablename__ = 'characteristic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('characteristic_type.id'), nullable=False, index=True)
    type = db.relationship('CharacteristicType', backref=db.backref('characteristictypes', lazy=True))

    def __str__(self):
        return self.name


class ProductDetail(db.Model):
    __tablename__ = 'product_detail'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('characteristic.id'), nullable=False, index=True)
    detail = db.relationship('Characteristic', backref=db.backref('characteristics', lazy=True))
    value = db.Column(db.String(100), nullable=False)
