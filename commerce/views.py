from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import generic
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Item, Cart
from .serializer import ItemSerializer, CartSerializer, ItemOrderSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def itemList(request, version):
    if request.method == 'GET':
        items = Item.objects.all()

        print(request.query_params)
        if(request.query_params.get('avail')):
            avail = int(request.query_params.get('avail'))
            items = Item.objects.filter(inventory_count__gt=0)
        serializer = ItemSerializer(items,many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method =='POST':
        # Purchase an item
        if version == 'v1':
            print(version)
            serializer = ItemOrderSerializer(data=request.data)
            if serializer.is_valid():
                item_order = serializer.save()

                try:
                    item = Item.objects.get(title=item_order.title)
                except Item.DoesNotExist:
                    return HttpResponse(status=400)

                diff = item.inventory_count - item_order.quantity

                #situation where requested quantity is too high
                #delete order and return not acceptable
                if diff < 0:
                    item_order.delete()
                    return JsonResponse(serializer.errors,status=406)

                item.inventory_count = diff
                item.save()

                #return created entry status
                return JsonResponse(serializer.data, status=201)

            return JsonResponse(serializer.errors, status=406)
        elif version == 'v2':
            #check command: create, update, complete
            try:
                command = request.data['command']
            except KeyError:
                return JsonResponse(status=401, data={'status':'false',
                            'message':'no command provided'})


            if command == 'create':
                serializer = CartSerializer(data=request.data)
                cart = serializer.save()

            #add item to cart (one at a time, or many)
            elif command == 'update':
                serializer = ItemOrderSerializer(data=request.data)
                items = serializer.save()

                try:
                    cart_id = request.data['id']
                    cart = Cart.objects.get(cart_id=cart_id)
                except KeyError:
                    return JsonResponse(status=401, data={'status':'false',
                                    'message':'cart not identified'})

                cart.items.create(title=items.title, quantity=items.quantity)

                #update cart value

            elif command == 'complete':
                try:
                    cart_id = request.data['id']
                    cart = Cart.objects.get(cart_id=cart_id)
                except KeyError:
                    return JsonResponse(status=401, data={'status':'false',
                                    'message':'no command provided'})

                #check if cart was already completed
                if cart.status == True:
                    return JsonResponse(status=400, data={'message:Cart already completed'})

                cart.status = True

                #update inventory:
                items = Cart.items.all()

                #update inventory for each item
                for item in items:
                    inventory_item = Item.objects.get(title=item.title)
                    diff = inventory_item.inventory_count - item.quantity
                    inventory_item.inventory_count = diff
                    inventory_item.save()


            try:
                complete_flag = request.data['complete']
            except KeyError:
                return JsonResponse(status=401, data={'status':'false',
                        'message':'cart not complete'})
            if complete_flag == 0:
                return JsonResponse(status=401, data={'status':'false',
                                        'message':'cart not complete'})
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():

                cart = serializer.save()
                items = cart.items.all()

                for item in items:
                    #update quantities
                    print(item.title)

                    #update items in inventory
                    try:
                        inventory_item = Item.objects.get(title=item.title)
                    except Item.DoesNotExist:
                        return JsonResponse(status=400,  data={'status':'false',
                                                'message':'Item not valid'})

                    diff = inventory_item.inventory_count - item.quantity

                    if(diff<0):
                        return JsonResponse(status=406,  data={'status':'false',
                                                'message':'no inventory'})

                    inventory_item.inventory_count = diff
                    inventory_item.save()

                    #return created entry status
                return JsonResponse(serializer.data, status=201)

            return JsonResponse(serializer.errors, status=406)

        else:
            return JsonResponse(status=400,data={'status':'false',
            'message':'no version specified'} )

@api_view(['GET'])
def detailItem(request, name, version):
    try:
        #perform some item cleaning
        clean_name = name.lower()
        print(clean_name)
        item = Item.objects.get(title=clean_name)
    except Item.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data, safe=False)
