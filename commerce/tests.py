from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Cart, Item, ItemOrder
from .serializer import ItemOrderSerializer, ItemSerializer
import json
import random

# tests for views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_Item(title, price, quantity ):
        if title != "" and price != 0 and quantity !=0:
            Item.objects.create(title=title, price=price, inventory_count=quantity)

    def setUp(self):
        # add test data
        self.create_Item('pen', 2.99, 100)
        self.create_Item('pencil', 5.99, 200)
        self.create_Item('paper', 1.99, 150)
        self.create_Item('erasor', 10.99, 19)
        self.create_Item('glue', 20.99, 0)
        self.create_Item('tape', 3.99, 0)


class GetItemsTest(BaseViewTest):

    def test_get_all_items(self):
        """
        Test getting all items through api call
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("commerce:itemlist", kwargs={'version':'v2'})
        )
        # fetch the data from db
        expected = Item.objects.all()
        serialized = ItemSerializer(expected, many=True)
        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_detail_item(self):
        # hit the API endpoint

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
        Ensure we can create a new account object.
        """
        url = reverse('commerce:itemlist', kwargs={'version':'v1'})
        data = {'title': 'pen', 'quantity':2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemOrder.objects.count(), 1)
        self.assertEqual(ItemOrder.objects.get().title, 'pen')

# class PlayerPostTestFail(APITestCase):
#     def test_fail_create_Player(self):
#         """
#         Ensure that with no auth, player does not get saved
#         """
#         url = reverse('mvp:playersList')
#         authenticated = 0
#         data = {'player_name': 'Kobe Bryant', 'player_team':'LALakers', 'complete':authenticated}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(Player.objects.count(), 0)
