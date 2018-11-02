from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse

from Orders.models import Order
from Orders.models import content

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
	return render(request,"confirm_order_view.html",{});
