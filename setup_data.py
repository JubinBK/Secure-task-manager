import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_task_manager.settings')
django.setup()

from vulnerable_app.models import VulnerableUser, Task, Comment
from secure_app.models import SecureTask, SecureComment
from django.contrib.auth.models import User

def setup_vulnerable_data():
    print("Setting up Vulnerable App Data...")
    admin_user, created = VulnerableUser.objects.get_or_create(username='admin', defaults={'password': 'adminpassword', 'email': 'admin@example.com', 'is_admin': True})
    if created: print("Created admin user")
    
    victim_user, created = VulnerableUser.objects.get_or_create(username='victim', defaults={'password': 'password123', 'email': 'victim@example.com', 'bio': 'I am a regular user.'})
    if created: print("Created victim user")

    attacker_user, created = VulnerableUser.objects.get_or_create(username='attacker', defaults={'password': 'hacker123', 'email': 'attacker@evil.com', 'bio': 'I am bad.'})
    if created: print("Created attacker user")

    t1, created = Task.objects.get_or_create(title='Secret Admin Task', defaults={'description': 'This is for admin eyes only.', 'assigned_to': admin_user})
    if created: print("Created Secret Admin Task")

    t2, created = Task.objects.get_or_create(title='Buy Milk', defaults={'description': 'Remember to buy milk.', 'assigned_to': victim_user})
    if created: print("Created Buy Milk Task")
    
    if not Comment.objects.filter(task=t2, author=attacker_user, content="<script>alert('XSS Attack!')</script>").exists():
        Comment.objects.create(task=t2, author=attacker_user, content="<script>alert('XSS Attack!')</script>")
        print("Created XSS Comment")
    
    print("Vulnerable Data Created.")

def setup_secure_data():
    print("Setting up Secure App Data...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    
    if not User.objects.filter(username='victim').exists():
        user = User.objects.create_user('victim', 'victim@example.com', 'password123')
        
        t1 = SecureTask.objects.create(title='Secure Task', description='This task is safe.', assigned_to=user)
        SecureComment.objects.create(task=t1, author=user, content='This is a safe comment.')

    print("Secure Data Created.")

if __name__ == '__main__':
    setup_vulnerable_data()
    setup_secure_data()
