from .models import FoodItem, Product, CartItem, Cart, Reservation
from datetime import time
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.exceptions import ValidationError
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    food_items = FoodItem.objects.all()[:3]
    products = Product.objects.all()[:3]
    context = {
        'food_items': food_items,
        'products': products
    }
    return render(request, 'home.html', context)


def menu(request):
    food_items = FoodItem.objects.all().order_by('category')
    food_items_grouped = {k: list(v) for k, v in groupby(food_items, key=attrgetter('category'))}
    return render(request, 'menu.html', {'food_items_grouped': food_items_grouped.items()})


def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def drinks(request):
    drink_items = FoodItem.objects.filter(category='Drinks').order_by('type')
    drink_items_grouped = {k: list(v) for k, v in groupby(drink_items, key=attrgetter('type'))}
    return render(request, 'drinks.html', {'drink_items_grouped': drink_items_grouped.items()})


def food(request):
    food_items = FoodItem.objects.all().filter(category='Food').order_by('type')
    food_items_grouped = {k: list(v) for k, v in groupby(food_items, key=attrgetter('type'))}
    return render(request, 'food.html', {'food_items_grouped': food_items_grouped.items()})


def contact(request):
    business_hours = [time(hour=10), time(hour=11), time(hour=12), time(hour=13),
                      time(hour=14), time(hour=15), time(hour=16), time(hour=17),
                      time(hour=18), time(hour=19), time(hour=20), time(hour=21)]

    selected_date = request.GET.get('date', None)
    if selected_date:
        existing_reservations = Reservation.objects.filter(date=selected_date)
    else:
        existing_reservations = Reservation.objects.none()

    available_times = []
    for t in business_hours:
        if not existing_reservations.filter(time=t).exists():
            available_times.append(t)

    return render(request, 'contact.html', {'available_times': available_times})


@login_required
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    items_with_subtotal = []
    for cart_item in user_cart.items.all():
        cart_item.subtotal = cart_item.quantity * cart_item.item.price
        items_with_subtotal.append(cart_item)
    
    user_cart.total = sum(item.subtotal for item in items_with_subtotal)
    user_cart.save()
    
    context = {
        'items_with_subtotal': items_with_subtotal,
        'total': user_cart.total,
    }
    return render(request, 'cart.html', context)


def item_detail(request, pk):
    item = FoodItem.objects.get(id = pk)
    return render(request, 'item_detail.html', {'item': item})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, pk, item_type):
    quantity = request.POST.get('quantity', 1)
    quantity = int(quantity)
    
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    
    model_class = None
    if item_type == 'food':
        model_class = FoodItem
    elif item_type == 'product':
        model_class = Product
    
    if model_class:
        content_type = ContentType.objects.get_for_model(model_class)
        item = get_object_or_404(model_class, pk=pk)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=item.pk,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        user_cart.items.add(cart_item)
        user_cart.save()
    else:
        pass
    
    return redirect('cart')


@require_POST
@login_required
def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    new_quantity = request.POST.get('quantity', 1)
    cart_item.quantity = int(new_quantity)
    cart_item.save()
    return redirect('cart')

@require_POST
@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart = Cart.objects.get(user=request.user)
    cart.items.remove(cart_item)
    cart_item.delete()
    return redirect('cart')


def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('home'))
    
    
@login_required
def create_checkout_session(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    items_with_subtotal = []
    for cart_item in user_cart.items.all():
        cart_item.subtotal = cart_item.quantity * cart_item.item.price
        items_with_subtotal.append(cart_item)
    
    user_cart.total = sum(item.subtotal for item in items_with_subtotal)
    user_cart.save()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'myr',
                    'product_data': {
                        'name': cart_item.item.name,
                    },
                    'unit_amount': int(cart_item.item.price * 100),
                },
                'quantity': cart_item.quantity,
            } for cart_item in items_with_subtotal],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        
        user_cart.items.clear()
        user_cart.save()
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        pass
    

def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')

def reserve(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    date = request.POST.get('date')
    time = request.POST.get('time')
    guests = request.POST.get('guests')

    reservation = Reservation(name=name, email=email, date=date, time=time, guests=guests)
    reservation.save()

    return redirect('reserved')
    

def reservation_success(request):
    return render(request, 'reserved.html')
