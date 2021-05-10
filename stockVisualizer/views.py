from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, RedirectView
from .forms import StockForm
from .models import Stock
import requests
import os
# Create your views here.

def home(request):
    try:
        stock = Stock.objects.all()
        data= list(Stock.objects.all())
        ticker = data[0]
        ticker = str(ticker).upper()
        apikey=os.getenv('alphavantage') # access our environmental variable with the os mdoule.
        sma = requests.get(f'https://www.alphavantage.co/query?function=SMA&interval=daily&time_period=10&series_type=close&symbol={str(data[0])}&apikey={apikey}').json()
        prices = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={str(data[0])}&apikey={apikey}').json()
        # Use the requests package to get our data from the Alpha Vantage API.
        # We want to try to access data in the database. However if it doens't exist our app still needs to work.
    except:
        stock = Stock.objects.all()
        data= list(Stock.objects.all())
        ticker = ''
        apikey=os.getenv('alphavantage')
        sma = ''
        prices = ''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StockForm(request.POST)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StockForm()

        return render(request, 'home.html',{
                'stock':stock,
                'ticker':ticker,
                'form':form,
                'sma':sma,
                'prices':prices,
                'apikey':apikey,
                # This dictionary is known as context in Django. It's useful to move data from the backend to your UI/frontend.
        })
# This function passes data from the frontend to the backend when a form is submitted. Also this passes data from our backend to our homepage when an http get request is made.

class StockView(RedirectView):
    url="/"
    # When we post data to our database this class redirects us back to our homepage

class StockUpdateView(UpdateView):
    model = Stock
    fields = ['symbol']
    template_name = 'stock_edit.html'
    # We will use this class to update our database Stock.symbol[0]

class StockCreateView(CreateView):
    model = Stock
    fields = ['symbol']
    template_name = 'stock_edit.html'
    # When nothing exists this class creates Stock.symbol[0]