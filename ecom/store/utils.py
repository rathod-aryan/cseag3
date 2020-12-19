import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
	    cart = {}
		
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping' :False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(name=i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
				'product':{
					'name':product.name,
					'price':product.price,
					'image':product.image,
				    },
				'quantity':cart[i]['quantity'],
				'get_total':total,
			    }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print("User is not logged in!")
    print("COOKIES: ", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer, 
        complete = False,
    )
    for item in items:
        product = Product.objects.get(name = item['product']['name'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order