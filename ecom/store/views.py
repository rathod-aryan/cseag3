from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.contrib import messages


from .models import *
from .utils import cookieCart, guestOrder
from .forms import CreateUserForm
import json
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
	else:
		customer, order = guestOrder(request, data)
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			pincode = data['shipping']['pincode'],
		)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()
	return JsonResponse('Payment Complete!', safe = False)

def signin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username,password=password)
		if user is not None :
			login(request, user)
			return redirect('store')
		else :
			messages.info(request, 'Incorrect Credentials. Please try again')
		

	context = {}
	return render(request, 'store/signin.html', context)

def signup(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = User.objects.get(username=form.cleaned_data.get('username'))
			fname = form.cleaned_data.get('first_name')
			lname = form.cleaned_data.get('last_name')
			name = fname + ' ' + lname
			email = form.cleaned_data.get('email')
			customer = Customer.objects.create(name = name, user = user, email=email)
			messages.success(request, 'Account Created!')
			return redirect('signin')
	

	context = {'form':form}
	return render(request, 'store/signup.html', context)

def signout(request):
	logout(request)
	return redirect('store')

