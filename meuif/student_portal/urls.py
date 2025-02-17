from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial
    path("", home, name="home"),  

    # Tasks
    path('user/tasks/', task_list, name='task_list'),
     path('user/tasks/new/', task_create, name='task_new'),
    path('user/tasks/<int:pk>/', task_detail, name='task_detail'),
    path('user/tasks/<int:pk>/edit/', task_edit, name='task_edit'),
    path('user/tasks/<int:pk>/done/', task_mark_done, name='task_mark_done'),
    path('user/profile/', profile_view, name='profile'),
    path('usertask/<int:pk>/delete/', task_delete, name='task_delete'),
    path('user/achievments', achievements_view, name='achievements'),


    # Usuário
    path("user/register/", user_new, name="register"),

    # Login e Logout
    path("login/", auth_views.LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]