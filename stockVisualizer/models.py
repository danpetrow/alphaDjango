from django.db import models
from django.urls import reverse

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=12)

    def __str__(self):
        return self.symbol

    def get_absolute_url(self):
        return reverse('stock', args=[str(self.id)])