"""alphaDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # this isn't even completly required but nice to have to look at the db *1
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # *1
    path('api/create/', views.StockCreateView.as_view(), name='stock_create'),
    path('api/ticker/<int:pk>', views.StockView.as_view(), name = "stock"),
    path('api/ticker/<int:pk>/edit/', views.StockUpdateView.as_view(), name='stock_edit'),
    path('', views.test, name='test')
]