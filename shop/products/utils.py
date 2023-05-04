from .models import Product, Brand, Category


def get_all_brands():
    return Brand.query.join(Product, (Brand.id == Product.brand_id)).all()


def get_all_categories():
    return Category.query.join(Product, (Category.id == Product.category_id)).all()

# сделать квадратной
# from PIL import Image  # $ pip install pillow
#
#
# def make_square(old_path, new_path, max_size=600, fill_color=(0, 0, 0)):
#     # find image dimensions
#     old_img = Image.open(old_path)
#     size = (min(max_size, max(old_img.size)),) * 2
#
#     # resize if old image is larger than max_size
#     if size[0] < old_img.size[0] or size[1] < old_img.size[1]:
#         old_img.thumbnail(size)
#
#     # create new image with the given color and computed size
#     new_img = Image.new(old_img.mode, size, fill_color)
#
#     # find coordinates of upper-left corner to center the old image in the new image
#     assert new_img.size[0] >= old_img.size[0]
#     assert new_img.size[1] >= old_img.size[1]
#
#     x = (new_img.size[0] - old_img.size[0]) // 2
#     y = (new_img.size[1] - old_img.size[1]) // 2
#
#     # paste image
#     new_img.paste(old_img, (x, y))
#
#     # save image
#     new_img.save(new_path)
#
#
# make_square('Снимок.PNG', 'pic1.png',max_size=1300,fill_color=(255,255,255))
