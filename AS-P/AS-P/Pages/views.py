from django.shortcuts import render
from Orders.models import Order
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
	obj = Order.objects.filter(status = "queued")
	context ={
		'object' : obj
	} 
	return render(request,"dispatcher_home_view.html",context);

def order_success_view(request, *args, **kwargs):
	return render(request,"order_success_view.html",{});

def confirm_order_view(request, *args, **kwargs):
	return render(request,"confirm_order_view.html",{});

