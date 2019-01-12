from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Cart, Item, ItemOrder
from .serializer import ItemOrderSerializer, ItemSerializer
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model


import json
import random

# tests for views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_Item(title, price, quantity ):
        if title != "" and price != 0 and quantity !=0:
            Item.objects.create(title=title, price=price, inventory_count=quantity)
    @staticmethod
    def create_Cart(name, total_val, status ):
        Cart.objects.create(cart_name=name, total_val=total_val,
            cart_status=status)


    def setUp(self):
        # add test data
        self.create_Item('pen', 2.99, 100)
        self.create_Item('pencil', 5.99, 200)
        self.create_Item('paper', 1.99, 150)
        self.create_Item('erasor', 10.99, 19)
        self.create_Item('glue', 20.99, 0)
        self.create_Item('tape', 3.99, 0)
        self.create_Cart('test', 0, 0)
        #user = User.objects.create_superuser(username="shopify", email="", password="testing21")
        self.user = get_user_model().objects.create_user('shopify', '', 'test')

class GetItemsTest(BaseViewTest):

    def test_get_all_items(self):
        """
        Test getting all items through api call
        """
        # user = User.objects.get(username='shopify')
        #
        # factory = APIRequestFactory()
        # request = factory.get(reverse("commerce:itemlist", kwargs={'version':'v2'}))
        #
        # force_authenticate(request,user=user, token=None)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("commerce:itemlist", kwargs={'version':'v2'}))

        #print(response.json())
        # fetch the data from db
        expected = Item.objects.all()
        serialized = ItemSerializer(expected, many=True)
        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_detail_item(self):
        """
        Test getting detail item through api call
        """
        self.client.force_authenticate(user=self.user)
        items = Item.objects.all()
        index = random.randint(0, len(items)-1)
        name = items[index].title
        response = self.client.get(
            reverse("commerce:detailitem", kwargs={'version':'v2', 'name': name })
        )

        expected = Item.objects.get(title = name)
        serialized = ItemSerializer(expected)
        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PurchasePostTest(BaseViewTest):
    def test_create_ItemOrder(self):
        """
        Ensure we can purchase one item on old version.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('commerce:itemlist', kwargs={'version':'v1'})
        data = {'title': 'pen', 'quantity':2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemOrder.objects.count(), 1)
        self.assertEqual(ItemOrder.objects.get().title, 'pen')


class PurchaseCartTest(BaseViewTest):
    def test_create_Cart(self):
        """
        Ensure we can create a new account object.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('commerce:itemlist', kwargs={'version':'v2'})
        new_cart = Cart.objects.all()
        new_cart.delete()

        data = {'command':'create', 'cart_name':'tests'}
        response = self.client.post(url, data, format='json')

        json_response = response.json()
        cart_id = int(json_response['cart_id'])


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().cart_id, cart_id)

    def test_update_Cart(self):
        """
        Ensure we can update a cart object.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('commerce:itemlist', kwargs={'version':'v2'})
        cart = Cart.objects.all()

        data = {'command':'update', 'cart_id':cart[0].cart_id, 'title':'pencil', 'quantity':5 }
        response = self.client.post(url, data, format='json')

        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemOrder.objects.count(), 1)
        self.assertEqual(ItemOrder.objects.get().title, 'pencil')

    def test_complete_Cart(self):
        """
        Ensure we can complete a cart object.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('commerce:itemlist', kwargs={'version':'v2'})
        cart = Cart.objects.all()
        data = {'command':'complete', 'cart_id': cart[0].cart_id}
        response = self.client.post(url, data, format='json')

        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().cart_status, 1)
