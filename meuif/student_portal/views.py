from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


# Listar Tasks (/user/tasks)
@login_required
def task_list(request):

    filter_status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)
    now = timezone.now()

    if filter_status == 'todo':
        tasks = tasks.filter(completed=False, due_date__gt=now)
    elif filter_status == 'overdue':
        tasks = tasks.filter(completed=False, due_date__lte=now)
    elif filter_status == 'done':
        tasks = tasks.filter(completed=True)

    return render(request, 'tasks/task_list.html', {"tasks": tasks})


# Deletar Tasks, minha melhor função. (/user/tasks/id-da-task/delete/)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# Criar Task (/user/tasks/new)

@login_required
def task_create(request):

    if request.method == "POST":

        form = TaskCreateForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
        
    else:
        form = TaskCreateForm()
    
    return render(request, 'tasks/task_create.html', {'form': form})

# Finaliza uma tarefa

@login_required
def task_mark_done(request, pk):

    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()
    return redirect('task_list')


# Editar uma task (/user/tasks/id-da-task/edit/)

@login_required
def task_edit(request, pk):

    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskEditForm(instance=task)
    
    return render(request, 'tasks/task_edit.html', {'form': form})


# Visualizar uma tarefa em detalhes (/user/tasks/id-da-task/)

@login_required 
def task_detail(request, pk):

    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


# Criar novo usuário(/user/register)
def user_new(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = RegisterForm()
    
    return render(request, "user/register.html", {"form": form})


# Rota para perfil do usuário(/user/register)

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")  
    else:
        form = UserUpdateForm(instance=user)

    total_completed_tasks = user.completed_tasks_count()

    return render(request, 'user/profile.html', {
        'user': user,
        'form': form,
        'total_completed_tasks': total_completed_tasks
    })


# Home page
def home(request):
    return render(request, "home/index.html")


# Visão das conquistas do usário
def achievements_view(request):

    all_achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user).values_list('achievement', flat=True)

    return render(request, 'user/achievements.html', {
        'achievements': all_achievements,
        'user_achievements': user_achievements
    })
