from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [

    # Task
    path("", home, name="home"),  # Define a página inicial
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('tasks/new/', task_new, name='task_new'),
    path('tasks/<int:pk>/edit/', task_edit, name='task_edit'),

    # User

    path("user/register/", user_new, name="register"),
    path("user/list/", user_list, name="user_list"),
    path("logout/", LogoutView.as_view(), name="logout"),

]

