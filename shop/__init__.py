import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate

# from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

# BASEDIR = os.path.abspath(os.path.dirname('__file__'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diploma_shop.db'
app.config['SECRET_KEY'] = 'sasadhgbwiuqhiuh3asda3sda3a'
#
app.config['UPLOAD_IMG_FOLDER'] = 'shop\static\images'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
# login_manager.login_message_category = 'danger'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Сначала авторизуйтесь"
login_manager.login_message_category = u"warning"

# must be after initialize
from shop.admin import routes
from shop.customers import routes
from shop.products import routes
from shop.carts import carts
# make db
from .admin.models import User
from .products.models import Brand, Category
from .customers.models import CustomerUser
from .carts.models import GoodsInCarts, Carts

# если не юзать flask-migrate
with app.app_context():
    db.create_all()
