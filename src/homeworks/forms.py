from django import forms
from .models import Task, Submission

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ("title", "description", "tips", "close_date", "answer")
