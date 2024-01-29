from django.db import models
from .user import User

class Order(models.Model):

    name = models.CharField(max_length=50)
    open = models.BooleanField(default=True)
    customer_phone = models.IntegerField()
    customer_email = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)
