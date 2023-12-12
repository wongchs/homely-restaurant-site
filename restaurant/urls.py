from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name="home"),
    path('catalog/', views.catalog, name="catalog"),
    path('menu/', views.menu, name="menu"),
    path('food/', views.food, name="food"),
    path('drinks/', views.drinks, name="drinks"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('add_to_cart/<item_type>/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    path('reserve/', views.reserve, name='reserve'),
    path('reserved/', views.reservation_success, name='reserved'),
]

