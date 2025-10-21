from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings


# Create your models here.
def today():
    return datetime.date.today()
class Habit(models.Model):
    def __str__(self):
        return self.title
    
    FREQUENCY_CHOICES=(
        ('Daily','Daily'),
        ('Weekly','Weekly')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1,related_name='habits')

    title=models.CharField(max_length=200)
    frequency=models.CharField(choices=FREQUENCY_CHOICES,default='daily')
    target=models. IntegerField(default=1)
    streaks=models.IntegerField(default=1)
    
class HabitCompletion(models.Model):
    
    name=models.ForeignKey(Habit,on_delete=models.CASCADE,related_name='completion')
    date=models.DateField(default=today)

    constraints=[
        models.UniqueConstraint(fields=['habit','date'],name='unique_habit_date')
        
    ]

    def __str__(self):
        return self.name.title