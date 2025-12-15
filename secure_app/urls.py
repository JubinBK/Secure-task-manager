from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='secure_register'),
    path('login/', auth_views.LoginView.as_view(template_name='secure_app/login.html'), name='secure_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='secure_login'), name='secure_logout'),
    path('tasks/', views.task_list, name='secure_task_list'),
    path('tasks/create/', views.task_create, name='secure_task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='secure_task_detail'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle_complete, name='secure_task_toggle'),
    path('profile/', views.profile_view, name='secure_profile'),
    path('users/', views.user_list, name='secure_user_list'),
    path('users/<int:user_id>/', views.user_edit, name='secure_user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='secure_user_delete'),
]
