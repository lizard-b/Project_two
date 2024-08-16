from coffee_shop.models import *

cat_1 = Category.objects.create(name='Кофейные молочные напитки')

product_1 = Product.objects.create(name="Латте, 300 мл", price=200.0, quantity=10, category=cat_1)
product_2 = Product.objects.create(name="Латте, 400 мл", price=290.0, quantity=10, category=cat_1)
