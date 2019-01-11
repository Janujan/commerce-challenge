from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import generic
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Item, Cart
from .serializer import ItemSerializer, CartSerializer, ItemOrderSerializer
from oauth2_provider.decorators import protected_resource

# Create your views here.
@protected_resource(scopes=['read', 'write'])
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
                    cart = serializer.save()
                    id = cart.cart_id
                    #cart.delete()
                    #return card_id
                    return JsonResponse({'cart_id':str(id)})
                else:
                    return JsonResponse(serializer.errors, status=400)

            #add item to cart (one at a time, or many)
            elif command == 'update':
                serializer = ItemOrderSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        cart_id = request.data['cart_id']
                        print(cart_id)
                        cart = Cart.objects.get(cart_id=cart_id)
                    except KeyError:
                        return JsonResponse(status=401, data={'status':'false',
                                        'message':'cart not identified'})

                    #check if cart was already completed
                    if cart.cart_status == True:
                        return JsonResponse(status=400, data={'message:Cart already completed'})

                    #check if item already exists, if so, just update quantity
                    new_item = serializer.save()

                    old_items = cart.items.filter(title=new_item.title)
                    title = new_item.title
                    quantity = new_item.quantity

                    #get item price also check if item is inventory
                    try:
                        price = Item.objects.get(title=new_item.title).price
                    except Item.DoesNotExist:
                        return JsonResponse({'message':'Item Does Not Exist'}, status=201)

                    #check if item already exists
                    if old_items:
                        prev_item = old_items[0]
                        prev_item.quantity += quantity
                        prev_item.save()
                        new_item.delete()
                    else:
                        print("new item")
                        new_item.cart = cart
                        new_item.save()

                    #update cart value
                    old_val = cart.total_val
                    new_val = old_val + new_item.quantity*price
                    cart.total_val = new_val
                    cart.save()

                    return JsonResponse(serializer.data, status=201)

                else:
                    return JsonResponse(serializer.errors, status=400)


            elif command == 'complete':
                print(request.data)
                try:
                    cart_id = request.data['cart_id']
                    print(cart_id)
                    cart = Cart.objects.get(cart_id=cart_id)
                except KeyError:
                    return JsonResponse(status=401, data={'status':'false',
                                    'message':'no command provided'})

                #check if cart was already completed
                if cart.cart_status == True:
                    return JsonResponse(status=304, data={'status':'false',
                            'message':'Cart already completed'})

                cart.cart_status = True
                cart.save()
                #update inventory:
                items = cart.items.all()

                #update inventory for each item
                for item in items:
                    inventory_item = Item.objects.get(title=item.title)
                    diff = inventory_item.inventory_count - item.quantity
                    inventory_item.inventory_count = diff
                    print(inventory_item.inventory_count)
                    inventory_item.save()

                return JsonResponse(data={'message':'cart complete!'}, status=201)

        else:
            return JsonResponse(status=400,data={'status':'false',
            'message':'no version specified'} )


@protected_resource(scopes=['read'])
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
