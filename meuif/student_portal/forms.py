from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Removemos o campo 'user'
        fields = ['name', 'score', 'max_score', 'weight', 'deadline']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        error_messages = {
            'password2': {
                'password_mismatch': "As senhas não coincidem.",
                'password_too_short': "A senha precisa ter pelo menos 8 caracteres.",
                # Você pode adicionar outros erros conforme a necessidade
            },
        }