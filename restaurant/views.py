from django.shortcuts import render
from django.http import HttpResponse
from .models import FoodItem
from itertools import groupby
from operator import attrgetter
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')


def menu(request):
    food_items = FoodItem.objects.all().order_by('category')
    food_items_grouped = {k: list(v) for k, v in groupby(food_items, key=attrgetter('category'))}
    return render(request, 'menu.html', {'food_items_grouped': food_items_grouped.items()})


def catalog(request):
    return render(request, 'catalog.html')


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
    return render(request, 'cart.html')


def item_detail(request, pk):
    item = FoodItem.objects.get(id = pk)
    return render(request, 'item_detail.html', {'item': item})

cart = []

def get_cart(request):
    # Your logic to fetch cart data goes here
    # For example, let's assume you have a list of items in the cart
    cart_data = [
        {'name': 'Product 1', 'price': 10.0, 'quantity': 2},
        {'name': 'Product 2', 'price': 5.0, 'quantity': 1},
        # Add more items as needed
    ]

    # Return a JSON response with cart data
    return JsonResponse(cart_data, safe=False)


def add_to_cart(request):
    # Dummy data for a new item to add to the cart
    new_item = {
        'name': request.GET.get('name', ''),
        'price': float(request.GET.get('price', 0)),
        'quantity': int(request.GET.get('quantity', 1)),
    }

    # Add the new item to the cart
    cart.append(new_item)

    # Return a JSON response indicating success
    return JsonResponse({'success': True})