from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import UpdateView, View, CreateView, RedirectView
from .forms import StockForm
from .models import Stock
import requests
# Create your views here.

def test(request):
    stock = Stock.objects.all()
    data= list(Stock.objects.all())
    ticker = data[0]
    sma = requests.get(f'https://www.alphavantage.co/query?function=SMA&interval=daily&time_period=10&series_type=close&symbol={str(data[0])}&apikey=3B8UZ3CBWOU6P33F').json()
    prices = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={str(data[0])}&apikey=3B8UZ3CBWOU6P33F').json()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StockForm(request.POST)
        # check whether it's valid:
       

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StockForm()

        return render(request, 'home_test.html',{
            'stock':stock,
            'ticker':ticker,
            'form':form,
            'sma':sma,
            'prices':prices,
        })

class StockView(RedirectView):
    url="/"

class StockUpdateView(UpdateView):
    model = Stock
    template_name = 'stock_edit.html'
    fields = ['symbol']

class StockCreateView(CreateView):
    model = Stock
    template_name = 'stock_edit.html'
    fields = ['symbol']