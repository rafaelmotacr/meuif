from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings  

class Task(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    name = models.CharField(max_length=128)
    score = models.FloatField(default=0.0)  
    max_score = models.FloatField(default=100.0)  
    weight = models.BigIntegerField()
    deadline = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name



class User(AbstractUser):  
    
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username  
    
