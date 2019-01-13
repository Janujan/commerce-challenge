from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import generic
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Item, Cart
from .serializer import ItemSerializer, CartSerializer, ItemOrderSerializer
from cart_ops import cartCreate, cartUpdate, cartComplete
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
                print(request.data)
                serializer = CartSerializer(data=request.data)
                if serializer.is_valid():
                    return cartCreate(serializer)
                else:
                    return JsonResponse(serializer.errors, status=400)

            elif command == 'update':
                serializer = ItemOrderSerializer(data=request.data)
                if serializer.is_valid():
                    return cartUpdate(serializer, request)
                else:
                    return JsonResponse(serializer.errors, status=400)

            elif command == 'complete':
                print(request.data)
                return cartComplete(request)

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
