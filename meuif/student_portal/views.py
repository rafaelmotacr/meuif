from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task, User, Achievement, UserAchievement
from .forms import *
from django.contrib import messages

# List all tasks
@login_required
def task_list(request):
    filter_status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)
    now = timezone.now()

    # Apply filters based on status
    if filter_status == 'todo':
        tasks = tasks.filter(completed=False, due_date__gt=now)
    elif filter_status == 'overdue':
        tasks = tasks.filter(completed=False, due_date__lte=now)
    elif filter_status == 'done':
        tasks = tasks.filter(completed=True)

    return render(request, 'tasks/task_list.html', {"tasks": tasks})


# Delete a task
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# Create a new task
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


# Mark a task as done
@login_required
def task_mark_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()
    return redirect('task_list')


# Edit an existing task
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


# View task details
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


# Register a new user
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


# User profile view

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")  # Certifique-se de que "profile" é o nome correto da URL
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


# Achievements view
def achievements_view(request):
    all_achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user).values_list('achievement', flat=True)

    return render(request, 'user/achievements.html', {
        'achievements': all_achievements,
        'user_achievements': user_achievements
    })
