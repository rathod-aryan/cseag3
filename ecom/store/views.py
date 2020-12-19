from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from .utils import cookieCart
import datetime


def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData= cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']	
	
	products = Product.objects.all()
	context = {'products':products, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		context = {'items':items, 'order':order, 'cartItems':cartItems}
	else:
		cookieData= cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']				
		context = {'items':items, 'order':order, 'cartItems':cartItems}
	
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		context = {'items':items, 'order':order, 'cartItems':cartItems}
	else:
		cookieData= cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']	
		context = {'items':items, 'order':order, 'cartItems':cartItems}
	
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	pname= data['pname']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(name=pname)
	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	
	
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action== 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	elif action== 'del':
		orderItem.quantity = 0

	orderItem.save()

	if orderItem.quantity <= 0 :
		orderItem.delete()
	return JsonResponse('Item was added',safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if (request.user.is_authenticated):
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				pincode = data['shipping']['pincode'],
			)
	else:
		print("User is not logged in!")
	return JsonResponse('Payment Complete!', safe = False)

def signin(request):
	context = {}
	return render(request, 'store/signin.html', context)

def signup(request):
	context = {}
	return render(request, 'store/signup.html', context)

def dashboard(request):
	context = {}
	return render(request, 'store/dashboard.html', context)

def fgtpsw(request):
	context = {}
	return render(request, 'store/fgtpsw.html', context)
