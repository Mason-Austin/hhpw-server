from django.db import models
from .order import Order

class Revenue(models.Model):

    total = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    payment_type = models.CharField(max_length=50)
    tip = models.DecimalField(max_digits=7, decimal_places=2)
    order_type = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
