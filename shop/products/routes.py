import os
import secrets
from sqlalchemy.sql import text, or_
from flask import render_template, redirect, request, url_for, flash, session, current_app, jsonify
from shop import db, app, search
from werkzeug.utils import secure_filename
from werkzeug.urls import url_encode
from .models import Brand, Category, Product, ProductDetail, Characteristic, CharacteristicType
from .utils import get_all_brands, get_all_categories
from .forms import AddProductForm
from flask_login import current_user


@app.route('/pr_char/<int:product_id>', methods=['GET'])
def pr_char(product_id):
    product_info = ProductDetail.query.filter(ProductDetail.product_id == product_id).all()
    dat = dict()
    for el in product_info:
        if (t := el.detail.type) not in dat:
            dat[t] = [{'name': el.detail, 'value': el.value}]
        else:
            dat[t].append({'name': el.detail, 'value': el.value})
    return jsonify({'output': render_template('test/characteristics.html', products_info=product_info, data=dat)})


@app.route('/product/<int:prod_id>', methods=["POST", "GET"])
def product_page(prod_id):
    product = Product.query.filter(Product.id == prod_id).first()
    return render_template('test/product_page.html', product=product, data=dict())


@app.route('/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', None)
    required_brands = request.args.getlist('brand')
    print(f'{sort=} {required_brands=} {page=}')

    if required_brands:
        br = Brand.query.filter(Brand.slug.in_(required_brands)).all()
        products_query = Product.query.filter(Product.brand_id.in_(g.id for g in br)).filter(Product.stock > 0)
    else:
        products_query = Product.query.filter(Product.stock > 0)
    if sort == 'pricedown':
        products = products_query.order_by(Product.price.desc()).paginate(page=page, per_page=4)
    elif sort == 'discount':
        products = products_query.order_by(Product.discount.desc()).paginate(page=page, per_page=4)
    else:
        products = products_query.order_by(Product.price.asc()).paginate(page=page, per_page=4)
    if request.method == 'POST':
        return jsonify({'output': render_template('products/catalog_products.html', products=products)})

    return render_template('products/index.html', products=products, brands=get_all_brands(),
                           categories=get_all_categories())


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Product.query.msearch(searchword, fields=['name', 'description'], limit=6)
    # limit сколько найдёт
    # TODO pagination
    if not searchword:
        return redirect(request.referrer)

    return render_template('products/result.html', products=products, brands=get_all_brands(),
                           categories=get_all_categories())


# @app.route('/get_brand/<int:brand_id>', methods=['GET'])
# def get_by_brand(brand_id):
#     page = request.args.get('page', 1, type=int)
#     get_br = Brand.query.filter_by(id=brand_id).first_or_404()
#     products_by_brand = Product.query.filter_by(brand=get_br).paginate(page=page, per_page=4)
#
#     return render_template('products/index.html', prod_by_brand=products_by_brand, brands=get_all_brands(),
#                            categories=get_all_categories(),
#                            get_br=get_br)

@app.route('/get_brand/<slug>', methods=['GET'])
def get_by_brand(slug):
    page = request.args.get('page', 1, type=int)
    get_br = Brand.query.filter_by(slug=slug).first_or_404()
    products_by_brand = Product.query.filter_by(brand=get_br).paginate(page=page, per_page=4)

    return render_template('products/index.html', prod_by_brand=products_by_brand, brands=get_all_brands(),
                           categories=get_all_categories(),
                           get_br=get_br)


@app.route('/test_brand', methods=['GET'])
def test_brand():
    print(request.args)
    print(request.url)
    print(request.values)
    print(request.full_path)
    page = request.args.get('page', 1, type=int)
    required_brands = request.args.getlist('brand')

    get_br = Brand.query.filter(Brand.slug.in_(required_brands)).all()
    products = Product.query.filter(Product.brand_id.in_(g.id for g in get_br)).paginate(page=page, per_page=4)
    # products = Product.query.filter_by(brand=get_br).paginate(page=page, per_page=4)
    return render_template('products/index.html', products=products, brands=get_all_brands(),
                           categories=get_all_categories(), get_br=get_br)


@app.route('/get_cat/<int:cat_id>', methods=['GET'])
def get_by_category(cat_id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=cat_id).first_or_404()
    products_by_category = Product.query.filter_by(category=get_cat).paginate(page=page, per_page=4)

    return render_template('products/index.html', products=products_by_category, brands=get_all_brands(),
                           categories=get_all_categories(), get_cat=get_cat)


@app.route('/addbrand', methods=['POST', 'GET'])
def add_brand():
    if request.method == 'POST':
        entered_brand: str = request.form.get('brand')
        new_brand: Brand = Brand(name=entered_brand)
        db.session.add(new_brand)
        db.session.commit()
        flash(f'The Brand "{entered_brand}" was added completely', 'success')
        return redirect(url_for('add_brand'))

    return render_template('products/add_brand.html', brands='brands', title='Add a brand')


@app.route('/update_brand/<int:brand_id>', methods=['POST', 'GET'])
def update_brand(brand_id: int):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    updated_brand = Brand.query.get_or_404(brand_id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updated_brand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/update_brand.html', title='Update brand', updated_brand=updated_brand)


@app.route('/delete_brand/<int:brand_id>', methods=['POST'])
def delete_brand(brand_id: int):
    brand = Brand.query.get_or_404(brand_id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} has been deleted', 'success')
        return redirect(url_for('brands'))
    flash(f'The brand cant be deleted', 'success')
    return redirect(url_for('brands'))


@app.route('/addcat', methods=['POST', 'GET'])
def add_category():
    if request.method == 'POST':
        entered_cat: str = request.form.get('category')
        new_category: Category = Category(name=entered_cat)
        db.session.add(new_category)
        db.session.commit()
        flash(f'The Category "{entered_cat}" was added completely', 'success')
        return redirect(url_for('add_category'))

    return render_template('products/add_brand.html', title='Add a category')


@app.route('/update_category/<int:cat_id>', methods=['POST', 'GET'])
def update_category(cat_id: int):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    updated_category = Category.query.get_or_404(cat_id)
    category = request.form.get('category')
    if request.method == 'POST':
        updated_category.name = category
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/update_brand.html', title='Update category', updated_category=updated_category)


@app.route('/delete_category/<int:cat_id>', methods=['POST'])
def delete_category(cat_id: int):
    category = Category.query.get_or_404(cat_id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The brand {category.name} has been deleted', 'success')
        return redirect(url_for('categories'))
    flash(f'The category cant be deleted', 'success')
    return redirect(url_for('categories'))


@app.route('/addproduct', methods=['POST', 'GET'])
def add_product():
    brands = Brand.query.all()
    categories = Category.query.all()
    detail_types = CharacteristicType.query.all()
    details = Characteristic.query.all()
    form = AddProductForm()
    if form.validate_on_submit():
        print('Тестовый кусок кода:')
        print(f'Тип Хар-ки: {request.form.getlist("details_type")}')
        print(f'Хар-ка: {request.form.getlist("details")}')
        print(f'Значение: {request.form.getlist("detail_value")}')
        print('------------------------------------')
        files_name = []
        files = [request.files.get(file) for file in request.files]
        for file in files:
            if file.filename == '':
                files_name.append('image.jpg')
                continue
            filename_ext = secure_filename(file.filename).split('.')[-1]
            filename = secrets.token_hex(10) + '.' + filename_ext
            path_to_save = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
            files_name.append(filename)
            file.save(path_to_save)

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        description = form.description.data
        new_product: Product = Product(name=name, price=price, discount=discount, stock=stock,
                                       brand_id=brand, category_id=category, description=description,
                                       image_1=files_name[0], image_2=files_name[1], image_3=files_name[2])
        db.session.add(new_product)
        db.session.commit()
        flash(f'Product {name} has been added successfully', 'success')

        # return redirect(request.url)
        return redirect(url_for('admin'))
    # print('Ошибки формы:', form.errors)

    return render_template('products/add_product.html', title='Добавление товара', form=form, brands=brands,
                           categories=categories, detail_types=detail_types, details=details)


@app.route('/update_product/<int:prod_id>', methods=['POST', 'GET'])
def update_product(prod_id):
    form = AddProductForm(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    updated_product = Product.query.get_or_404(prod_id)

    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        updated_product.name = form.name.data
        updated_product.price = form.price.data
        updated_product.discount = form.discount.data
        updated_product.stock = form.stock.data
        updated_product.description = form.description.data
        updated_product.brand_id = brand
        updated_product.category_id = category
        # TODO refactor code for pattern DRY - MUST REFACTOR
        if form.validate_on_submit():
            have_new_file = False
            files_name = []
            files = [request.files.get(file) for file in request.files]
            for file in files:
                if file.filename != '':
                    have_new_file = True
            if have_new_file:
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/images/' + updated_product.image_1))
                    for file in files:
                        if file.filename == '':
                            files_name.append('image.jpg')
                            continue
                        filename_ext = secure_filename(file.filename).split('.')[1]
                        filename = secrets.token_hex(10) + '.' + filename_ext
                        path_to_save = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
                        files_name.append(filename)
                        file.save(path_to_save)
                    if have_new_file:
                        updated_product.image_1 = files_name[0]
                        updated_product.image_2 = files_name[1]
                        updated_product.image_3 = files_name[2]
                except Exception as ex:
                    print('NETU')
                    files_name = []
                    files = [request.files.get(file) for file in request.files]
                    for file in files:
                        if file.filename == '':
                            files_name.append('image.jpg')
                            continue
                        filename_ext = secure_filename(file.filename).split('.')[1]
                        filename = secrets.token_hex(10) + '.' + filename_ext
                        path_to_save = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
                        files_name.append(filename)
                        file.save(path_to_save)
                    if have_new_file:
                        updated_product.image_1 = files_name[0]
                        updated_product.image_2 = files_name[1]
                        updated_product.image_3 = files_name[2]
        print(form.errors)
        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = updated_product.name
    form.price.data = updated_product.price
    form.discount.data = updated_product.discount
    form.stock.data = updated_product.stock
    form.description.data = updated_product.description

    return render_template('products/update_product.html', title='Обновить товар', form=form, product=updated_product,
                           brands=brands, categories=categories)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id: int):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        # TODO refactor DRY

        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))

        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
        except:
            print('FILE NOT FOUND')
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
        except:
            print('FILE NOT FOUND')

        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'The product cant be deleted', 'success')
    return redirect(url_for('admin'))
