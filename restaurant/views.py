from django.shortcuts import render
from django.http import HttpResponse


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
    return render(request, 'food.html')


def contact(request):
    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')