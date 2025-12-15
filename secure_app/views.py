from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import SecureTask, SecureComment
from .forms import SecureRegistrationForm, SecureTaskForm, SecureCommentForm

def register(request):
    if request.method == 'POST':
        form = SecureRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('secure_task_list')
    else:
        form = SecureRegistrationForm()
    return render(request, 'secure_app/register.html', {'form': form})

@login_required
def task_list(request):
    search_query = request.GET.get('q')
    tasks = SecureTask.objects.filter(assigned_to=request.user)
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    return render(request, 'secure_app/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = SecureTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            messages.success(request, "Task created.")
            return redirect('secure_task_list')
    else:
        form = SecureTaskForm()
    return render(request, 'secure_app/task_form.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(SecureTask, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        form = SecureCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('secure_task_detail', task_id=task.id)
    else:
        form = SecureCommentForm()
    
    comments = task.comments.all()
    return render(request, 'secure_app/task_detail.html', {'task': task, 'comments': comments, 'form': form})

@login_required
def task_toggle_complete(request, task_id):
    task = get_object_or_404(SecureTask, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        status = "completed" if task.completed else "pending"
        messages.success(request, f"Task marked as {status}.")
        return redirect('secure_task_detail', task_id=task.id)
    
    return redirect('secure_task_detail', task_id=task.id)

@login_required
def profile_view(request):
    return render(request, 'secure_app/profile.html', {'user': request.user})

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.only('id', 'username', 'email', 'is_superuser').all()
    return render(request, 'secure_app/user_list.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user_to_edit.email = request.POST.get('email')
        user_to_edit.first_name = request.POST.get('first_name')
        user_to_edit.last_name = request.POST.get('last_name')
        
        if request.POST.get('is_superuser'):
            user_to_edit.is_superuser = True
            user_to_edit.is_staff = True
        else:
            if user_to_edit != request.user:
                user_to_edit.is_superuser = False
                user_to_edit.is_staff = False
                
        user_to_edit.save()
        messages.success(request, f"User {user_to_edit.username} updated.")
        return redirect('secure_user_list')
        
    return render(request, 'secure_app/user_edit.html', {'user_to_edit': user_to_edit})

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('secure_user_list')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User {username} has been deleted.")
        return redirect('secure_user_list')
    
    return render(request, 'secure_app/user_confirm_delete.html', {'user_to_delete': user_to_delete})
