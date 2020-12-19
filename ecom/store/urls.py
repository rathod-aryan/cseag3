from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="processs_order"),
	path('signin/', views.signin, name="signin"),
	path('signout/', views.signout, name="signout"),
	path('signup/', views.signup, name="signup"),
]