from django.db import models

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField( default = 0)
    inventory_count = models.IntegerField( default = 0)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True, max_length=30)
    total_val = models.FloatField(default= 0)
    cart_name = models.CharField(max_length=200)
    cart_status = models.BooleanField(default=False)

class ItemOrder(models.Model):
    cart = models.ForeignKey(Cart, related_name= 'items', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
