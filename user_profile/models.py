from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    
     age=models.IntegerField(null=True ,blank=True)
     daily_goals=models.IntegerField(default=1)
     
     def __str__(self):
          return self.username