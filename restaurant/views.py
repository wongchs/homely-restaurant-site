from django.shortcuts import render
from django.http import HttpResponse
from .models import FoodItem
from itertools import groupby
from operator import attrgetter


# Create your views here.
def home(request):
    return render(request, 'home.html')


def menu(request):
    return render(request, 'menu.html')


def catalog(request):
    return render(request, 'catalog.html')


def about(request):
    return render(request, 'about.html')


def drinks(request):
    return render(request, 'drinks.html')


def food(request):
    food_items = FoodItem.objects.all().order_by('type')
    food_items_grouped = {k: list(v) for k, v in groupby(food_items, key=attrgetter('type'))}
    return render(request, 'food.html', {'food_items_grouped': food_items_grouped.items()})


def contact(request):
    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')