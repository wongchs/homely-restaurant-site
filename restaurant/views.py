from django.shortcuts import render
from django.http import HttpResponse
from .models import FoodItem
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, get_object_or_404
from .models import Product


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
    return render(request, 'cart.html')


def item_detail(request, pk):
    item = FoodItem.objects.get(id = pk)
    return render(request, 'item_detail.html', {'item': item})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})