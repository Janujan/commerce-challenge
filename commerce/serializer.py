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
    items = ItemOrderSerializer(many=True)
    class Meta:
        model = Cart
        fields = ("cart_name")

    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     cart = Cart.objects.create(**validated_data)
    #     for item_data in items_data:
    #         ItemOrder.objects.create(cart = cart, title=item_data['title'], quantity=item_data['quantity'])
    #     return cart
