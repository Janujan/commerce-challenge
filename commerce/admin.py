from django.contrib import admin

from .models import Cart, Item, ItemOrder
# Register your models here.

admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(ItemOrder)
