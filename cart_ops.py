from commerce.models import Cart, ItemOrder, Item
from commerce.serializer import CartSerializer, ItemOrderSerializer, ItemSerializer
from django.http import HttpResponse, JsonResponse

def cartCreate( serializer ):
	cart = serializer.save()
	id = cart.cart_id
	return JsonResponse({'cart_id':str(id)})


def cartUpdate( serializer, request ):
	try:
		cart_id = request.data['cart_id']
		print('cart_id in update')
		print(Cart.objects.all()[0].cart_id)
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


def cartComplete( request ):
	try:
		cart_id = request.data['cart_id']
		print('cart id')
		print(cart_id)
		print(Cart.objects.all()[0].cart_id)
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
		inventory_item.save()

	return JsonResponse(data={'message':'cart complete!'}, status=201)
