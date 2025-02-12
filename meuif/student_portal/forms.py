from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user', 'name', 'score', 'max_score', 'weight', 'deadline']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]  # Use os campos corretos do Django
