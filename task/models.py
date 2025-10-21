from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth.models import User
import random 
from django.conf import settings
# Create your models here.

import random
def next_date():
   
   return datetime.date.today() + datetime.timedelta(days=random.randint(3,7))
   
class Task(models.Model):
    def __str__(self):
        return self.title
    
    PRIORITY_CHOICE=(
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low')
    )
    STATUS_CHOICE=(
        ('Pending','Pending'),
        ('Done','Done')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1,related_name='tasks')


    title=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    priority=models.CharField(choices=PRIORITY_CHOICE)
    due_date=models.DateField(default=next_date) 
    status=models.CharField(choices=STATUS_CHOICE,default='Pending')