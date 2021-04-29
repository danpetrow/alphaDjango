Build a Stock Data Visualizer Web App Using Alpha Vantage + Django
---

In this tutorial we will build a simple web app to visualize stock data using Python, Django, and the Alpha Vantage API. This demonstration was done using Windows but the process will be similar for Mac or linux.

Get an Alpha Vantage API key
https://www.alphavantage.co/support/#api-key
Get and Install Python if you don't already have it 
https://www.python.org/downloads/

Open up your command prompt.

Install Django
	>>> C:\Users\dppet\Desktop\ $pip install django

Create a project directory and the skeleton for your project.
    >>> C:\Users\dppet\Desktop\ django-admin startproject alphaDjango 

Then open up your project dir
    >>> C:\Users\dppet\Desktop\ cd alphaDjango


Create a new app
    >>> C:\Users\dppet\Desktop\alphaDjango python manage.py startapp stockVisualizer
    
Setup your database
    >>> python manage.py migrate

Your first view
    >>> C:\Users\dppet\Desktop\alphaDjango\stockVisualizer\views.py
    
    #views.py
    from django.shortcuts import render
    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Hello, world. This is a stock visualizer")

Your first URL
    >>> C:\Users\dppet\Desktop\alphaDjango\stockVisualizer\urls.py
    
    #stockVisualizer\urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index),
    ]
        
Your project's URLs
    >>> C:\Users\dppet\Desktop\alphaDjango\urls.py
    
    #alphaDjango\urls.py
    from django.urls import include, path

    urlpatterns = [
        path('', include('stockVisualizer.urls')),
    ]

Let's make sure that everything is working up to this point.
    >>> C:\Users\dppet\Desktop\alphaDjango\ python manage.py runserver
    
    Open up your webbrowser and navigate to http://localhost:8000
    ![alphaDjango.png](attachment:image.png)

--- Break---

Now let's make some html.
    >>> C:\Users\dppet\Desktop\alphaDjango\ mkdir templates
    >>> C:\Users\dppet\Desktop\alphaDjango\ cd templates
    >>> C:\Users\dppet\Desktop\alphaDjango\templates type nul >> "home.html" # this works will in powershell but might not work in command prompt
    
Now we need to edit one part of our settings to use the html file.
    >>> C:\Users\dppet\Desktop\alphaDjango\settings.py
    
    #alphaDjango/settings.py
    import os
    
    INSTALLED_APPS = [
    ...
    'stockVisualizer', #add this
]

    templates = [
        {
        'DIRS': [os.path.join(BASE_DIR, 'templates') #add this],
        },
    ] 
    #There will be other stuff in this file that you will not want to change but you need to add to the file.

---
Placeholder create a model, then run py manage.py makemigrations && py manage.py migrate    

stockVisualizer/models.py

    from django.db import models

    # Create your models here.
    class Stock(models.Model):
        symbol = models.CharField(max_length=12)

        def __str__(self):
            return self.symbol

python manage.py makemigrations 
python manage.py migrate

python manage.py createsuperuser

stockVisualizer/admin.py
    from django.contrib import admin
    from .models import Stock
    # Register your models here.

    admin.site.register(Stock)