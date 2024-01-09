from django.db import models
from .order import Order

class Revenue(models.Model):

    total = models.FloatField()
    date = models.DateField(auto_now_add=True)
    payment_type = models.CharField(max_length=50)
    tip = models.FloatField()
    order_type = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
