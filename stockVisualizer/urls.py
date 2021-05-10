#from django.contrib import admin # this isn't even completly required but nice to have to look at the db *1
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls), # *1
    path('api/create/', views.StockCreateView.as_view(), name='stock_create'),
    path('api/ticker/<int:pk>', views.StockView.as_view(), name = "stock"),
    path('api/ticker/<int:pk>/edit/', views.StockUpdateView.as_view(), name='stock_edit'),
    path('', views.home, name='home')
]