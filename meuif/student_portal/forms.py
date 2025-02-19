from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import Task, User

class TaskCreateForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Due Date'
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'completed': 'Completed',
        }


class TaskEditForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Due Date'
    )
    completed_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Completion Date',
        required=False
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'completed_at']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'completed': 'Completed',
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        error_messages = {
            'password2': {
                'password_mismatch': "As senhas não coincidem.",
                'password_too_short': "A senha precisa ter pelo menos 8 caracteres.",
            },
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
