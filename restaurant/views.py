from .models import FoodItem, Product, CartItem, Cart
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def home(request):
    return render(request, 'home.html')


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


def cart(request):
    cart = request.session.get('cart', {'items': [], 'total': 0})
    
    items_with_subtotal = []
    for item_info in cart['items']:
        pk = item_info['pk']
        item_type = item_info['type']
        
        if item_type == 'food':
            item = FoodItem.objects.get(pk=pk)
            content_type = ContentType.objects.get_for_model(FoodItem)
        elif item_type == 'product':
            item = Product.objects.get(pk=pk)
            content_type = ContentType.objects.get_for_model(Product)
        else:
            continue
        cart_item = CartItem(content_type=content_type, object_id=item.pk, quantity=1)
        cart_item.subtotal = cart_item.quantity * item.price
        items_with_subtotal.append(cart_item)
    
    cart['total'] = sum(item.subtotal for item in items_with_subtotal)
    
    context = {
        'items_with_subtotal': items_with_subtotal,
        'total': cart['total'],
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


def add_to_cart(request, pk, item_type):
    cart = request.session.get('cart', {'items': [], 'total': 0})
    cart['items'].append({'pk': pk, 'type': item_type})
    request.session['cart'] = cart
    return redirect('cart')


def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    new_quantity = request.POST.get('quantity', 1)
    cart_item.quantity = int(new_quantity)
    cart_item.save()
    return redirect('cart')


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