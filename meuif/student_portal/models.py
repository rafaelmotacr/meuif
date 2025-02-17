from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Modelo de user

class User(AbstractUser):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def completed_tasks_count(self):
        return self.tasks.filter(completed=True).count()

    def __str__(self):
        return self.username


# Modelo de tasks

class Task(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)


    def mark_done(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save()
        check_achievements(self.user) 


    def get_status(self):
        now = timezone.now()
        if self.completed:
            return 'Concluída'
        elif now > self.due_date:
            return 'Atrasada'
        else:
            return 'Por Fazer'


def check_achievements(user):

    completed_tasks = Task.objects.filter(user=user, completed=True).count()
    delayed_tasks = Task.objects.filter(user=user, completed=True, completed_at__gt=models.F("due_date")).count()
    early_tasks = Task.objects.filter(user=user, completed=True, completed_at__lt=models.F("due_date")).count()

    all_achievements = Achievement.objects.all()
    for achievement in all_achievements:

        if achievement.name == "Procrastinador Nato" and delayed_tasks >= achievement.condition:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)

        elif achievement.name == "Apressadinho" and early_tasks >= achievement.condition:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)

        elif achievement.condition <= completed_tasks:
            UserAchievement.objects.get_or_create(user=user, achievement=achievement)


# Modelo de conquistas

class Achievement(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.IntegerField(help_text="Número de tarefas para desbloquear esta conquista.")

    def __str__(self):
        return self.name


# Tabela N pra N entre user e achievments

class UserAchievement(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
