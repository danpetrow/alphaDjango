from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Stock
# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. This is a stock visualizer")

class StockListView(ListView):
    model = Stock
    template_name = 'home.html'

class StockView(DetailView):
    model = Stock
    template_name = 'stock.html'