from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import HttpResponse

from Orders.models import Order
from Orders.models import content
from client.models import cart
from users.models import user

from Inventory.models import Item
# Create your views here.

def add_cart_view(request, *args, **kwargs):
	obj = Item.objects.get(item_id=1)
	context = {
		'object' : obj
	}
	return render(request,"add_cart_view.html", context);

def client_home_view(request, *args, **kwargs):
	return render(request,"client_home_view.html",{});

def dispatcher_home_view(request, *args, **kwargs):
	
	get_params = request.GET
	print(get_params)
	if 'view_details' in get_params:
		view_details = request.GET.get('view_details',-1)
	
		if view_details != '-1':
			print()
			print()
			print(view_details)
			print()
			print()
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
			print()
			print()
			print("entered change status")
			print()
			print()
			order_to_update = Order.objects.get(order_id=changeStatus)
			order_to_update.status = "Dispatched"
			order_to_update.save()

	obj = Order.objects.filter(status = "Queued for Dispatch")
	print(obj)
	context ={
		'object' : obj
	} 
	
	return render(request,"dispatcher_home_view.html",context);

def order_success_view(request, *args, **kwargs):
	return render(request,"order_success_view.html",{});

def confirm_order_view(request, *args, **kwargs):
	print(request.method)
	print(request.GET.get("BACK"))
	print(request.GET)
	Account = user.objects.get(username = "TEST")
	obj = cart.objects.filter(username = Account)
	print(obj)
	get_params = request.GET
	if 'BACK' in get_params:
		Goback = request.GET.get("BACK")
		if Goback == '-1':
			return redirect('../client_home_view/')


	if 'Really' in get_params:
		answer = request.GET.get('Priority')
		print(answer)
		Makeorder = Order.objects.create(orderID = 3, owner = Account, status="Queued for processing", priority = answer)
		for oneitem in obj:
			p = content.objects.create(username=Account, item_id=oneitem.item, quantity=oneitem.quantity, orderID=Makeorder)
		orderInfo ={
			'orderID' : Makeorder
		}
		return render(request, "order_success_view.html", orderInfo)


	totalweight = 0;
	for oneitem in obj:
		totalweight += oneitem.item.weight*oneitem.quantity
	context ={
		'object' : obj,
		'weight' : totalweight
	}

	return render(request,"confirm_order_view.html",context);

