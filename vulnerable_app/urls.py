from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='vulnerable_register'),
    path('login/', views.login_view, name='vulnerable_login'),
    path('logout/', views.logout_view, name='vulnerable_logout'),
    path('tasks/', views.task_list, name='vulnerable_task_list'),
    path('tasks/create/', views.task_create, name='vulnerable_task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='vulnerable_task_detail'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle_complete, name='vulnerable_task_toggle'),
    path('profile/', views.profile_update, name='vulnerable_profile'),
    path('users/', views.user_list, name='vulnerable_user_list'),
    path('users/<int:user_id>/', views.user_edit, name='vulnerable_user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='vulnerable_user_delete'),
]
