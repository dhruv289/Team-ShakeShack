from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import HttpResponse

from Orders.models import Order
from Orders.models import content

from users.models import user

from client.models import cart

from Inventory.models import Item
# Create your views here.
import csv

from decimal import Decimal

from datetime import datetime

def add_cart_view(request, *args, **kwargs):
	
	item_id=request.GET.get('item_id','invalid')
	username=request.GET.get('username','invalid')
	obj = Item.objects.get(item_id=item_id)
	context = {
		'username': username,
		'object' : obj
	}
	return render(request,"add_cart_view.html", context);

def client_home_view(request, *args, **kwargs):


	get_params = request.GET
	username = request.GET.get('username','invalid')
	#print(get_params)
	if 'Quantity' in get_params:
		quantity = request.GET.get('Quantity','invalid')
		int_quantity = int(quantity)
		item_id = request.GET.get('item_id','invalid')
		user_id = user.objects.get(username = username)
		item = Item.objects.get(item_id=item_id)
		
		weight = item.weight * int_quantity
		print( "The weight is: " +str(weight))
		new_cart_object = cart(username=user_id,item = item,quantity = quantity,shipping_weight = weight)
		new_cart_object.save()	

	total = Decimal(0.00)
	if username != 'invalid':
		client = user.objects.get(username = username)
		items = cart.objects.filter(username=client)
		for present_item in items:
			total = total + present_item.shipping_weight
		
	obj = Item.objects.all()

	if 'category' in get_params:
		category = request.GET.get('category','invalid')
		obj = Item.objects.filter(category = category)

	if 'search' in get_params:
		keyword = request.GET.get('search', 'invalid')
		obj = Item.objects.filter(name__icontains = keyword)
	
	object = {'object': items, 'username': username, 'items': obj, 'total_weight': total}
	return render(request,"client_home_view.html",object);

def dispatcher_home_view(request, *args, **kwargs):
	
	get_params = request.GET
	print(get_params)
	if 'view_details' in get_params:
		view_details = request.GET.get('view_details',-1)
	
		if view_details != '-1':
			order = Order.objects.get(order_id=view_details)
			order_content=content.objects.filter(orderID=order)
			print(order_content)
			return render(request,"order_details_view.html",{
				'order_num': view_details,
				'status': "Queued for Dispatch",
				'order_content':order_content
				})

	if 'changeStatus' in get_params:
		changeStatus = request.GET.get('changeStatus',-1)
		print(changeStatus)
		if changeStatus != '-1' :
			order_to_update = Order.objects.get(order_id=changeStatus)
			order_to_update.status = "Dispatched"
			order_to_update.dispatch_time = datetime.now()
			order_to_update.save()


	if 'download' in get_params:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
		writer = csv.writer(response)
		writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
		writer.writerow(['Second row', 'A', 'B', 'C'])
		return response
	

	obj = Order.objects.filter(status = "Queued for Dispatch")
	print(obj)
	context ={
		'object' : obj
	} 
	
	return render(request,"dispatcher_home_view.html",context);

def order_success_view(request, *args, **kwargs):

 	get_order_id = request.GET.get('order_id', -1)
 	obj = Order.objects.get(order_id=get_order_id)
 	context = { 'object': obj}
 	return render(request, "order_success_view.html", context)

def confirm_order_view(request, *args, **kwargs):
	#print(request.method)
	#print(request.GET.get("BACK"))
	#print(request.GET)
	username = request.GET.get('username','invalid')
	Account = user.objects.get(username = username)
	obj = cart.objects.filter(username = Account)
	print(obj)
	get_params = request.GET
	if 'BACK' in get_params:
		Goback = request.GET.get("BACK")
		if Goback == '-1':
			return redirect('../client_home_view?username='+username)


	if 'Really' in get_params:
		answer = request.GET.get('Priority')
		Lastorder = Order.objects.latest('order_id')
		Makeorder = Order.objects.create(order_id = Lastorder.order_id+1, owner = Account, status="Queued for processing", priority = answer)
		for oneitem in obj:
			p = content.objects.create(username=Account, item_id=oneitem.item, quantity=oneitem.quantity, orderID=Makeorder)
		orderInfo ={
			'order_id' : Makeorder
		}
		return render(request, "order_success_view.html", orderInfo)


	totalweight = 0;
	for oneitem in obj:
		totalweight += oneitem.item.weight*oneitem.quantity
	context ={
		'object' : obj,
		'weight' : totalweight,
		'username' : username
	}

	return render(request,"confirm_order_view.html",context);

