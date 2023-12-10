from .models import FoodItem, Product, CartItem, Cart
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST


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
    return render(request, 'contact.html')


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


def checkout(request):
    return render(request, 'checkout.html')


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


@login_required
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid login credentials'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid registration data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})