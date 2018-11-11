from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import HttpResponse

from Orders.models import Order
from Orders.models import content

from users.models import user

from client.models import cart

from Inventory.models import Item

from dispatcher.models import Drone, Drones_content
# Create your views here.
import csv

from Location_Data.models import Distance
from Location_Data.models import Location

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

def csv_generator(clinics):
        userName=cart.objects.all()
        users=user.objects.all()
        print(userName.values("username"))
        
        #print(users.values("username"))
        #clinics=list()
        #for obj in userName.values_list("username",flat=True):
        #        print (obj)
        #        if obj in users.values_list("username",flat=True):
        #                print(obj)
        #                clinic.appends(user.objects.get(username=obj))
        #clinics.append("A")
        #clinics.append("B")
        #clinics.append("C")
        #clinics.append("D")
        print (clinics)
        distance=Distance.objects.all()
        placeA=distance.values_list("placeA",flat=True)
        placeB=distance.values_list("placeB",flat=True)
        distance=Distance.objects.filter(placeA="Queen Mary Hospital Drone Port",placeB=clinics[0])
        print(distance.values_list("distance",flat=True))
        loop=len(clinics)
        print(loop)
        travel=list()
        minDistance=999
        clinic1=0
        for clin in clinics:
                if clin in placeB:
                        distance=Distance.objects.filter(placeA="Queen Mary Hospital Drone Port",placeB=clin)
                        for i in distance.values_list("distance",flat=True):
                                if minDistance>i:
                                                minDistance=i
                                                clinic1=clin
        for i in range(loop-1):
                minDistance=999
                for clinic2 in clinics:
                        if clinic1 in placeA and clinic2 in placeB:
                                distance=Distance.objects.filter(placeA=clinic1,placeB=clinic2)
                                for i in distance.values_list("distance",flat=True):
                                        if minDistance>i:
                                                minDistance=i
                                                nextClinic=clinic1
                                                nowClinic=clinic2
                                                print(minDistance)
                clinics.remove(nextClinic)
                travel.append(nextClinic)
                clinic1=nowClinic
        travel.append(clinics[0])
        travel.append("Queen Mary Hospital Drone Port")
        print(travel)
        location=Location.objects.all()
        #altitudes=location.values_list("altitude",flat=True)
        names=location.values_list("name",flat=True)
        #print(altitudes)
        alt=list()
        for clinic in travel:
                if clinic in names:
                        altitudes=Location.objects.filter(name=clinic)
                        for altitude in altitudes.values_list("altitude",flat=True):
                                alt.append(altitude)
        print (alt)                                
        context={
                'object':travel
        }

        return travel

def dispatcher_home_view(request, *args, **kwargs):
	
	get_params = request.GET
	#print(get_params)
	if 'view_details' in get_params:
		view_details = request.GET.get('view_details',-1)
	
		if view_details != '-1':
			order = Order.objects.get(order_id=view_details)
			order_content=content.objects.filter(orderID=order)
			#print(order_content)
			return render(request,"order_details_view.html",{
				'order_num': view_details,
				'status': "Queued for Dispatch",
				'order_content':order_content
				})

	if 'changeStatus' in get_params:
		changeStatus = request.GET.get('changeStatus',-1)
		if changeStatus != '-1' :
			order_to_update = Order.objects.get(order_id=changeStatus)
			order_to_update.status = "Dispatched"
			order_to_update.dispatch_time = datetime.now()
			order_to_update.save()
			drone_list = Drone.objects.all()
			flag = 0
			for present_drone in drone_list:
				if order_to_update.weight+present_drone.present_weight <=25:
					flag=1
					present_drone.present_weight=present_drone.present_weight+order_to_update.weight
					present_drone.save()
					new_content = Drones_content(drone=present_drone,order=order_to_update)
					print("first save is stopped")
					new_content.save()
			if flag == 0:
				new_drone_num = Drone.objects.all().count()+1
				new_drone = Drone(drone_num= new_drone_num, present_weight=order_to_update.weight)
				new_drone.save()
				new_content = Drones_content(drone=new_drone,order=order_to_update)
				print ("second save is stopped")
				new_content.save()

	if 'download' in get_params:
		drone_num = request.GET.get("drone_num","invalid")
		drone = Drone.objects.get(drone_num=drone_num)
		order_list = Drones_content.objects.filter(drone=drone)
		print("This is the order list")
		print(order_list)
		clinic_list = list()
		for present_order in order_list:
			clinic_list.append(present_order.order.owner.location.name)

		iteniary = csv_generator(clinic_list)
		print("The following is the iteniary")
		print(iteniary)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="route.csv"'
		writer = csv.writer(response)
		for present_location in iteniary:
			writer.writerow([present_location])
			present_location_data = Location.objects.get(name=present_location)
			print(present_location)
			writer.writerow(["longitude: ",present_location_data.longitude])
			writer.writerow(["latitude: ",present_location_data.latitude])
			writer.writerow(["altitude: ", present_location_data.altitude])
			writer.writerow([])
			writer.writerow([])
		return response
	

	obj = Order.objects.filter(status = "Queued for Dispatch", priority="HIGH")
	order_content_med=Order.objects.filter(status = "Queued for Dispatch", priority="MEDIUM")
	order_content_low=Order.objects.filter(status = "Queued for Dispatch", priority="LOW")
	print(obj)
	context ={
		'object' : obj,
		'order_content_med':order_content_med,
		'order_content_low': order_content_low
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
	totalweight = 0
	get_params = request.GET
	if 'BACK' in get_params:
		Goback = request.GET.get("BACK")
		if Goback == '-1':
			return redirect('../client_home_view?username='+username)

	if 'Really' in get_params:
		
		for oneitem in obj:
			totalweight += oneitem.item.weight*oneitem.quantity
		answer = request.GET.get('Priority')
		new_order_num = Order.objects.all().count()+1

		Makeorder = Order.objects.create(order_id = new_order_num, owner = Account, status="Queued for processing", priority = answer, weight=totalweight)
		for oneitem in obj:
			p = content.objects.create(username=Account, item_id=oneitem.item, quantity=oneitem.quantity, orderID=Makeorder)
			oneitem.delete()
		orderInfo ={
			'order_id' : Makeorder
		}
		return render(request, "order_success_view.html", orderInfo)

	for oneitem in obj:
		totalweight += oneitem.item.weight*oneitem.quantity
	
	context ={
		'object' : obj,
		'weight' : totalweight,
		'username' : username
	}

	return render(request,"confirm_order_view.html",context);

