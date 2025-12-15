from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .models import VulnerableUser, Task, Comment
from .forms import LoginForm, RegistrationForm, TaskForm, CommentForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vulnerable_login')
    else:
        form = RegistrationForm()
    return render(request, 'vulnerable_app/register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            query = f"SELECT * FROM vulnerable_app_vulnerableuser WHERE username = '{username}' AND password = '{password}'"
            
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchone()
            
            if user:
                request.session['user_id'] = user[0]
                request.session['username'] = user[1]
                request.session['is_admin'] = bool(user[5])
                return redirect('vulnerable_task_list')
            else:
                return render(request, 'vulnerable_app/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'vulnerable_app/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('vulnerable_login')

def task_list(request):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    search_query = request.GET.get('q')
    if search_query:
        query = f"SELECT * FROM vulnerable_app_task WHERE title LIKE '%{search_query}%'"
        tasks = Task.objects.raw(query)
    else:
        tasks = Task.objects.all()
    
    return render(request, 'vulnerable_app/task_list.html', {'tasks': tasks})

@csrf_exempt
def task_create(request):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to_id = request.session['user_id']
            task.save()
            return redirect('vulnerable_task_list')
    else:
        form = TaskForm()
    return render(request, 'vulnerable_app/task_form.html', {'form': form})

@csrf_exempt
def task_detail(request, task_id):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'vulnerable_app/404.html', {'message': 'Task not found'})

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author_id = request.session['user_id']
            comment.save()
            return redirect('vulnerable_task_detail', task_id=task.id)
    else:
        form = CommentForm()
    
    comments = task.comments.all()
    return render(request, 'vulnerable_app/task_detail.html', {'task': task, 'comments': comments, 'form': form})

@csrf_exempt
def task_toggle_complete(request, task_id):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return render(request, 'vulnerable_app/404.html', {'message': 'Task not found'})
    
    task.completed = not task.completed
    task.save()
    return redirect('vulnerable_task_detail', task_id=task.id)

@csrf_exempt
def profile_update(request):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
        
    try:
        user = VulnerableUser.objects.get(id=request.session['user_id'])
    except VulnerableUser.DoesNotExist:
        request.session.flush()
        return redirect('vulnerable_login')
    
    if request.method == 'POST':
        user.bio = request.POST.get('bio', user.bio)
        user.email = request.POST.get('email', user.email)
        
        if 'is_admin' in request.POST:
            user.is_admin = True
            
        user.save()
        return redirect('vulnerable_task_list')
        
    return render(request, 'vulnerable_app/profile.html', {'user': user})

@csrf_exempt
def user_list(request):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    try:
        current_user = VulnerableUser.objects.get(id=request.session['user_id'])
    except VulnerableUser.DoesNotExist:
        request.session.flush()
        return redirect('vulnerable_login')
        
    if not current_user.is_admin:
        return render(request, 'vulnerable_app/404.html', {'message': 'Access denied'})
        
    users = VulnerableUser.objects.only('id', 'username', 'email', 'is_admin').all()
    return render(request, 'vulnerable_app/user_list.html', {'users': users})


@csrf_exempt
def user_edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    try:
        current_user = VulnerableUser.objects.get(id=request.session['user_id'])
    except VulnerableUser.DoesNotExist:
        request.session.flush()
        return redirect('vulnerable_login')
        
    if not current_user.is_admin:
        return render(request, 'vulnerable_app/404.html', {'message': 'Access denied'})

    try:
        user_to_edit = VulnerableUser.objects.get(id=user_id)
    except VulnerableUser.DoesNotExist:
        return render(request, 'vulnerable_app/404.html', {'message': 'User not found'})
    
    if request.method == 'POST':
        user_to_edit.username = request.POST.get('username')
        user_to_edit.email = request.POST.get('email')
        user_to_edit.bio = request.POST.get('bio')
        if request.POST.get('is_admin'):
            user_to_edit.is_admin = True
        else:
            user_to_edit.is_admin = False
        user_to_edit.save()
        return redirect('vulnerable_user_list')
        
    return render(request, 'vulnerable_app/user_edit.html', {'user_to_edit': user_to_edit})

@csrf_exempt
def user_delete(request, user_id):
    if 'user_id' not in request.session:
        return redirect('vulnerable_login')
    
    try:
        current_user = VulnerableUser.objects.get(id=request.session['user_id'])
    except VulnerableUser.DoesNotExist:
        request.session.flush()
        return redirect('vulnerable_login')
        
    if not current_user.is_admin:
        return render(request, 'vulnerable_app/404.html', {'message': 'Access denied'})
    
    try:
        user_to_delete = VulnerableUser.objects.get(id=user_id)
        user_to_delete.delete()
    except VulnerableUser.DoesNotExist:
        return render(request, 'vulnerable_app/404.html', {'message': 'User not found'})
    return redirect('vulnerable_user_list')
