from .models import Habit
from django import forms

class HabitForm(forms.ModelForm):
    class Meta:
        model=Habit
        fields=['title','frequency','target']

