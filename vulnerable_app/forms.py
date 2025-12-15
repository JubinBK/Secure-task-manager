from django import forms
from .models import VulnerableUser, Task, Comment

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = VulnerableUser
        fields = ['username', 'password', 'email', 'bio']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
