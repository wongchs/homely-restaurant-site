from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('catalog/', views.catalog, name="catalog"),
    path('menu/', views.menu, name="menu"),
    path('food/', views.food, name="food"),
    path('drinks/', views.drinks, name="drinks"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart")
]

