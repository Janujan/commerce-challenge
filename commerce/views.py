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
        """
        Return a list of all items depending on query string
        """"

        items = Item.objects.all()

        if(request.query_params.get('avail')):
            avail = int(request.query_params.get('avail'))
            items = Item.objects.filter(inventory_count__gt=0)
        serializer = ItemSerializer(items,many=True)
        return JsonResponse(serializer.data, safe=False)


    elif request.method =='POST':
        if version == 'v1':
            """
            Purchase a single item
            """"

            serializer = ItemOrderSerializer(data=request.data)
            if serializer.is_valid():
                item_order = serializer.save()

                try:
                    item = Item.objects.get(title=item_order.title)

                except Item.DoesNotExist:
                    item_order.delete()
                    return JsonResponse(data={
                                'status':'error',
                                'message':'Item doesnt exist'
                                }, status=400)

                diff = item.inventory_count - item_order.quantity

                #situation where requested quantity is too high
                if diff < 0:
                    item_order.delete()
                    return JsonResponse(data={
                            'status':'error',
                            'message':'quantity too high'
                            }, status=400)

                item.inventory_count = diff
                item.save()

                #return created entry status
                return JsonResponse(serializer.data, status=201)

            return JsonResponse(serializer.errors, status=400)
        elif version == 'v2':
            """
            Cart Posting
            Needs to have one of the following commands:
            - create
            - update
            - complete
            """
            try:
                command = request.data['command']
            except KeyError:
                return JsonResponse(data={
                            'status':'error',
                            'message':'no command provided'
                            }, status=401)


            if command == 'create':
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
                return cartComplete(request)


        else:
            return JsonResponse(data={
                        'status':'error',
                        'message':'no version specified'
                        }, status=400 )

@api_view(['GET'])
def detailItem(request, name, version):
    """
    Return a single item depending on name that is passed
    """"
    try:
        #perform some item name cleaning
        clean_name = name.lower()
        item = Item.objects.get(title=clean_name)
        
    except Item.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data, safe=False)
