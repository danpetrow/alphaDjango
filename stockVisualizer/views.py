from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, View, CreateView, RedirectView
from .forms import StockForm
from .models import Stock
import requests
# Create your views here.

def get_data(request, *args, **kwargs):
    data= list(Stock.objects.all())
    j = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={str(data[0])}&apikey=3B8UZ3CBWOU6P33F').json()
    return JsonResponse(j)

def get_sma_data(request, *args, **kwargs):
    data= list(Stock.objects.all())
    j = requests.get(f'https://www.alphavantage.co/query?function=SMA&interval=daily&time_period=10&series_type=close&symbol={str(data[0])}&apikey=3B8UZ3CBWOU6P33F').json()
    return JsonResponse(j)

def test(request):
    stock = Stock.objects.all()
    data= list(Stock.objects.all())
    ticker = data[0]
    j = requests.get(f'https://www.alphavantage.co/query?function=SMA&interval=daily&time_period=10&series_type=close&symbol={str(data[0])}&apikey=3B8UZ3CBWOU6P33F').json()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StockForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.cleaned_data(symbol)
            stock.update(form.symbol)
            return redirect('test')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StockForm()

        return render(request, 'home_test.html',{
            'stock':stock,
            'ticker':ticker,
            'form':form,
            'j':j,
        })

class StockListView(ListView):
    model = Stock
    template_name = 'home.html'
    field = ['symbol']

class StockView(RedirectView):
    url="/"
"""
class StockView(DetailView):
    model = Stock
    template_name = 'stock.html'
    fields = ['symbol']
"""        
class StockUpdateView(UpdateView):
    model = Stock
    template_name = 'stock_edit.html'
    fields = ['symbol']

class StockCreateView(CreateView):
    model = Stock
    template_name = 'stock_edit.html'
    fields = ['symbol']