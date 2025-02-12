from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import User 

# Lista todas as Tasks

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Apenas tarefas do usuário logado
    return render(request, 'tasks/task_list.html', {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Atribui o usuário logado
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})


@login_required
def task_edit(request, pk):
    # Garante que o usuário só possa editar suas próprias tarefas
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})
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
