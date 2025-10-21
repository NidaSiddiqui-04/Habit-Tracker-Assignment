from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','priority','due_date']
class TaskStatus(forms.ModelForm):
    class Meta:
        model=Task
        fields=['status']    