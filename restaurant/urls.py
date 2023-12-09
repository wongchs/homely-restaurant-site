from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('catalog/', views.catalog, name="catalog"),
    path('menu/', views.menu, name="menu"),
    path('food/', views.food, name="food"),
    path('drinks/', views.drinks, name="drinks"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('add_to_cart/<item_type>/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.custom_register, name='register'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart')
]

