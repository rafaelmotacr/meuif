from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import login, authenticate
from .models import User 

# Lista todas as Tasks
def task_list(request):
    return render(request, 'tasks/task_list.html', {})


# Exibe os detalhes de uma Task específica
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


# Cria uma nova Task via formulário
def task_new(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_date = timezone.now()  # Define a data de criação
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})


# Edita uma Task existente


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})


# User

def user_new(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva corretamente o usuário
            login(request, user)  # Faz login automático
            return redirect("task_list")  
        else:
            print("Erro no formulário:", form.errors)  # Depuração no terminal

    else:
        form = RegisterForm()
    
    return render(request, "user/register.html", {"form": form})  # Ajuste conforme necessário


def user_list(request):
    users = User.objects.all()  # Obtém todos os usuários cadastrados
    return render(request, 'user/user_list.html', {"users": users})  # Passa para o template


def home(request):
    return render(request, "home/index.html")
