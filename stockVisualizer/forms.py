from django import forms

class StockForm(forms.Form):
    symbol = forms.CharField(label='Stock Ticker', max_length=12)