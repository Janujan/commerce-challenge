from rest_framework import serializers
from .models import Item, Cart, ItemOrder


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("title","price","inventory_count")

class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = ("title", "quantity")

class CartSerializer(serializers.ModelSerializer):
    #items = ItemOrderSerializer(many=True)
    class Meta:
        model = Cart
        fields = ("cart_name",)
