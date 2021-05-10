# Build a Stock Data Visualizer Web App Using Alpha Vantage + Django

---

In this tutorial we will build a simple web app to visualize stock data using Python (Django), Javascript, and the Alpha Vantage API. What we are going to visualize is Simple Moving Average, Daily Close, and Daily Adjusted Close for a given stock. 

If you are new to stocks you might be curious, what is the difference between Daily Close and Daily Adjusted Close? Daily Close is the last price that a stock was traded at for a particular day. Daily Adjusted Close is the last price that a stock was traded at for a particular day minus any corporate actions taken that would affect a stock price. That is to say that if a corporation pays dividends, splits their stock, issues rights, spins-off a new independent company ect. it is useful to discount the Daily Close price to account for this hidden value that was given to investors.

This tutorial is meant for an audience with a basic understanding of coding but it should also be valuable if you have no experience coding.

---

I've broken down our application into four main sections. In the Models section we will be creating a sqllite backend database. While this project could be done without a backend a database is essential to any modern web application. In the Views section we tell our application what to do when it recieves http requests. In the Templates section we create our html, css, and javascript. The Misc section covers settings and other housekeeping items.

## Index

- [Conventions](#Conventions)
- [Getting Started Installing Requirements](#Getting Started Installing Requirements)
- [[#Models]]
- [[#Views]]
- [[#Templates]]
- [[#Misc]]

This demonstration was done using Windows but the process will be similar for Mac or linux. This is by no means a definitive guide to Django but it should be a great entry point for someone looking to quickly build their first app.

---
## Conventions
A block that starts with a > indicates a command that should be run in your terminal or command prompt. Make sure you're running the terminal as Administrator.

	> pip install Django
	
Blocks that start with a # followed by a path indicate that we are working with (creating/editing) a file. I use Visual Studio Code but you can use any text editor or IDE of you choosing.

	#C:\Users\dppet\Desktop\alphaDjango\stockVisualizer\views.py

---
## Getting Started
- [Get an Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)
- [Install Python if you don't already have it](https://www.python.org/downloads/)
- Install Django
`> pip install Django`
- Install Requests
`> pip install requests`
---
Create a Windows Environment Variable for your apikey

	> setx alphavantage yourapikeygoeshere

Create a project directory and the skeleton for your project.

    > C:\Users\dppet\Desktop\ django-admin startproject alphaDjango 

Then open up your project dir

    > C:\Users\dppet\Desktop\ cd alphaDjango

Create a new app

    > C:\Users\dppet\Desktop\alphaDjango python manage.py startapp stockVisualizer

---
## Models
Define the structure of your data

	from django.db import models
	from django.urls import reverse

	# Create your models here.

	class Stock(models.Model):
    	symbol = models.CharField(max_length=12)
	# If you are familar with SQL what we are doing here is creating a table called stock which has a column called symbol where we will store some data
	
    def __str__(self):
        return self.symbol
	# Create a method that returns a string of the data in our symbol column.
	
    def get_absolute_url(self):
        return reverse('stock', args=[str(self.id)])
	# This creates a unique url for us to access each item in our database. 
	
Instantiate your database

    > C:\Users\dppet\Desktop\alphaDjango python manage.py migrate
	# You should notice running this migrate command creates db.sqlite3 file in your base directory (C:\Users\dppet\Desktop\alphaDjango)
	
Create a form from your database model.
	
	# C:\Users\dppet\Desktop\alphaDjango\stockVisualizer\forms.py
	from django import forms

	class StockForm(forms.Form):
		 symbol = forms.CharField(label\='Stock Ticker', max\_length\=12)
 
---
## Views

Your first view

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

Your first URL
    
    #C:\Users\dppet\Desktop\alphaDjango\stockVisualizer\urls.py
    from django.contrib import admin # this isn't even completly required but nice to have to look at the db *1
	from django.urls import path
	from . import views

	urlpatterns = [
		path('admin/', admin.site.urls), # *1
		path('api/create/', views.StockCreateView.as_view(), name = 'stock_create'),
		path('api/ticker/<int:pk>', views.StockView.as_view(), name = "stock"),
		path('api/ticker/<int:pk>/edit/', views.StockUpdateView.as_view(), name = 'stock_edit'),
		path('', views.home, name = 'home')
	]
	
Your project's URLs
    
    #C:\Users\dppet\Desktop\alphaDjango\urls.py
    from django.urls import include, path

    urlpatterns = [
        path('', include('stockVisualizer.urls')),
    ]
---
## Templates
Django uses a a technology called Jinja which allows you to write reusable html components. If you're familiar with html but see something like {% block content %} or {{ stock }} just know this is Jinja.

Now let's make some html.

    > C:\Users\dppet\Desktop\alphaDjango\ mkdir templates
    > C:\Users\dppet\Desktop\alphaDjango\ cd templates
    > C:\Users\dppet\Desktop\alphaDjango\templates\ type nul >> "home.html" # this works will in powershell but might not work in command prompt
	
An html base
	
	# C:\Users\dppet\Desktop\alphaDjango\templates\base.html
	<!DOCTYPE html>
	<html lang="en" style="height: 100%; overflow:hidden;">
	<head>
		<!--<link rel="stylesheet" href="style.css">-->
		<script src="https://cdn.jsdelivr.net/npm/chart.js@3.2.1/dist/chart.min.js"></script>
		<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
		<title>{% block title %}My amazing site{% endblock %}</title>
	</head>

	<body style='height: 100%;'>
		<nav><a href="/">Home</a></nav>
		<div id="content">      
			{% block content %}{% endblock %}
		</div>
	</body>
	</html>
    
Homepage html, css, and Javascript.

	# C:\Users\dppet\Desktop\alphaDjango\templates\home.html
	{% extends 'base.html' %}

	{% block content %}

    {% for symbol in stock  %}
    {% empty %}
        <h1>Search</h1>
        <form action = {% url 'stock_create' %} method="post">{% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update" />
        </form>
    {% endfor  %}

    {% for symbol in stock %}
        {% if symbol.pk == 1 %}
        <div style='height:10%;'>
        <div style="display:inline-block">
        <h1>Search</h1>
        </div>
        <div style="display:inline-block">
        <form action = {% url 'stock_edit' symbol.pk %} method="post" id="myForm" float='left'>{% csrf_token %}
        {{ form }}
        <input type="submit" value="Update" />
        </form>
        </div>
        </div>
        {% endif %}
    {% endfor %}
    <div style="height:90%; width:90%;">
    <canvas id="myChart"></canvas>
    </div>

    <script>
        //variables
        var ticker = "{{ ticker }}"
        var apikey = "{{ apikey }}"
        //console.log(apikey)
        var endpoint = 'https://www.alphavantage.co/query?function=SMA&interval=daily&time_period=10&series_type=close&symbol='+ticker+'&apikey='+apikey
        var endpoint1 = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol='+ticker+'&apikey='+apikey
        let dates, sma, daily_adjusted_close, daily_close, lo = []
        //document ready function
        
        res1 = $(document).ready(function(){
            //more variables
            //lo = []
            //dates = []
            //sma = []
            //daily_adjusted_close = []
            daily_close = []
            //ajax call 1
            $.ajax({
                method: "GET",
                url: endpoint,
                crossDomain: true,
                success: function(data){
                    i=data['Technical Analysis: SMA']
                    ting = function(){
                        var ii = []
                        dates = []
                        sma = []
                        for (let key in i) {
                            dates.push(String(key))
                            lo.push(i[key])
                            ;}
                        for (let key in lo) {
                        sma.push(Number(lo[key]['SMA']))
                        ;}
                        //console.log(dates)
                        //console.log(sma)
                        //return{
                        //    dates: dates,
                        //    sma: sma,
                        //}
                    ;}
                    //console.log(ting.dates)
                //var results = 
                ting()
                //console.log(results)
                //return results
                },
                error: function(error_data){
                console.log("error")}
            });
            //console.log(success.results)
            // second get
            $.ajax({
                method: "GET",
                url: endpoint1,
                crossDomain: true,
                success: function(data){
                    //make vars
                    testing = []
                    daily_close = []
                    daily_adjusted_close = []
                    var i = data['Time Series (Daily)']
                    // get daily close
                    daily_close_parse = function(){
                        for (let key in i) {
                            daily_close.push(Number(i[key]['4. close']))
                        ;}
                    ;}
                    daily_close_parse()
                    daily_adjusted_close_parse = function(){
                        for (let key in i) {
                            daily_adjusted_close.push(Number(i[key]['5. adjusted close']))
                        ;}
                    }
                    daily_adjusted_close_parse()

                    //sanity check
                    //var testing = dates.length-daily_close.length
                    //console.log(testing)
                    //console.log(daily_close.slice(0,testing).length)
                    //console.log(daily_close.slice(0,-5))
                    //console.log(dates)
                    //fixing the order of the data
                    daily_adjusted_close.reverse().slice(60)
                    daily_close.reverse().slice(60)
                    dates.reverse().slice(60)
                    sma.reverse().slice(60)
                    //make a graph
                    var ctx = document.getElementById('myChart').getContext('2d');
                    var myChart = new Chart(ctx, {
                    type: 'line',
                        data: {
                            labels: dates.slice(-60),
                            datasets: [{
                                label: 'Simple Moving Average',
                                data: sma.slice(-60),
                                backgroundColor: [
                                    'rgba(99, 132, 255, 0.2)',
                                ],
                                borderColor: [
                                    'rgba(99, 132, 255, 1)',
                                ],
                                borderWidth: 1
                            },
                            {
                                label: 'Daily Close',
                                data: daily_close.slice(-60),
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.2)',
                                ],
                                borderColor: [
                                    'rgba(255, 99, 132, 1)',
                                ],
                                borderWidth: 1
                            },
                            {
                                label: 'Daily Adjusted Close',
                                data: daily_adjusted_close.slice(-60),
                                backgroundColor: [
                                    'rgba(99, 255, 132, 0.2)',
                                ],
                                borderColor: [
                                    'rgba(99, 255, 132, 1)',
                                ],
                                borderWidth: 1
                            },
                        ]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: {
                                    //beginAtZero: false
                                }
                            },
                            plugins: {
                                legend: {
                                position: 'top',
                                },
                                title: {
                                display: true,
                                text: ticker
                                }
                            }
                        }
                    });
                },
                error: function(error_data){
                console.log("error")}
            });

        });
        </script>
	{% endblock content %}
	
Html for editing our database
	
	# C:\Users\dppet\Desktop\alphaDjango\templates\stock_edit.html
	{% extends 'base.html' %}

	{% block content %}
			<h1>Search</h1>
			<form action = "" method="post">{% csrf_token %}
			{{ form.as_p }}
			<input type="submit" value="Update" />
			</form>
	{% endblock content %}

---

## Misc

Now we need to edit one part of our settings to make the app work.
    
    #C:\Users\dppet\Desktop\alphaDjango\settings.py
    import os #add this
    ...
    INSTALLED_APPS = [
    ...
    'stockVisualizer', #add this
	]
	...
    TEMPLATES = [
		...
        {
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #add this
        },
		...
    ] 
    #There will be other stuff in this file that you will not want to change but you need to add to the file.

---
Congrats you've made a webapp with Python, Javascript, and Alphavantage! Run your application so we can take a look at your work.

	> C:\Users\dppet\Desktop\alphaDjango\ python manage.py runserver

Open up [http://localhost:8000/](http://localhost:8000/)