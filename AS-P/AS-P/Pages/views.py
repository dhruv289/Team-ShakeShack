from django.shortcuts import render

# Create your views here.

def add_cart_view(request, *args, **kwargs):
	return render(request,"add_cart_view.html",{});

def client_home_view(request, *args, **kwargs):
	return render(request,"client_home_view.html",{});

def dispatcher_home_view(request, *args, **kwargs):
	return render(request,"dispatcher_home_view.html",{});

def order_success_view(request, *args, **kwargs):
	return render(request,"order_success_view.html",{});

def confirm_order_view(request, *args, **kwargs):
	return render(request,"confirm_order_view.html",{});

