"""Model for user"""
from django.db import models

class User(models.Model):
    """Model for user"""
    uid = models.CharField(max_length=50)
    