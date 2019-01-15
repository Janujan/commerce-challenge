import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopifychallenge.settings")
django.setup()

from commerce.models import Item
import random


def freshLoad(item_names, item_quantities, item_prices):
    for x in range(0,10):
        item = Item.objects.create(title=item_names[x],
         inventory_count=item_quantities[x], price=item_prices[x])
        print(item)

def reLoad(item_names, item_quantities, item_prices):
    for x in range(0,10):
        item = Item.objects.get(title=item_names[x])
        item.quantity = item_quantities[x]
        item.save()
        print(item)

item_names = ['pen', 'pencil', 'paper', 'eraser', 'stapler',
        'backpack', 'notebook', 'scissors', 'calendar', 'ruler']

item_quantities = [ 1000, 77, 0, 7, 0, 1111, 950, 667, 0, 41 ]

item_prices = [ 7.99, 5.99, 4.89, 5.70, 6.80, 2.99, 1.77, 8.20, 1.20, 4.20 ]

#freshLoad(item_names, item_quantities, item_prices)
reLoad(item_names, item_quantities, item_prices)
