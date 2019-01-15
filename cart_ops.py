from commerce.models import Cart, ItemOrder, Item
from commerce.serializer import CartSerializer, ItemOrderSerializer, ItemSerializer
from django.http import HttpResponse, JsonResponse
import six
def cartCreate( serializer ):
	cart = serializer.save()
	id = cart.cart_id
	return JsonResponse({'cart_id':str(id)})


def cartUpdate( serializer, request ):
	try:
		cart_id = request.data['cart_id']
		#ensure that cart is a number
		if isinstance(cart_id, six.string_types):
	 		raise KeyError('string input as cart_id')

		cart = Cart.objects.get(cart_id=cart_id)
	except KeyError:
		return JsonResponse(status=400, data={'status':'error',
						'message':'cart not identified'})

	#check if cart was already completed
	if cart.cart_status == True:
		return JsonResponse(status=400, data={'status':'error','message':'Cart already completed'})

	#check if item already exists, if so, just update quantity
	new_item = serializer.save()

	old_items = cart.items.filter(title=new_item.title)
	title = new_item.title
	quantity = new_item.quantity

	#get item price also check if item is inventory
	try:
		price = Item.objects.get(title=new_item.title).price
		inventory_count = Item.objects.get(title=new_item.title).inventory_count

	except Item.DoesNotExist:
		new_item.delete()
		return JsonResponse({'status':'error','message':'Item Does Not Exist'}, status=400)


	if old_items:
		quantity += old_items[0].quantity

	#check if quantity is being exceeded
	if quantity > inventory_count:
		new_item.delete()
		return JsonResponse(status=400, data={'status':'error',
										'message':'quantity is too high'})

	#check if item already exists
	if old_items:
		prev_item = old_items[0]
		prev_item.quantity += quantity
		prev_item.save()
		new_item.delete()
	else:
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
		cart = Cart.objects.get(cart_id=cart_id)
	except Cart.DoesNotExist:
		return JsonResponse(status=400, data={'status':'error',
									'message':'cart id error'})
	except KeyError:
			return JsonResponse(status=400, data={'status':'error',
										'message':'cart id error'})
	#check if cart was already completed
	if cart.cart_status == True:
		return JsonResponse(status=400, data={'status':'error',
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

	return JsonResponse(data={'message':'cart complete!', 'Total Value': cart.total_val}, status=201)
