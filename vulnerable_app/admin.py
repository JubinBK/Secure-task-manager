from django.contrib import admin
from .models import VulnerableUser, Task, Comment

admin.site.register(VulnerableUser)
admin.site.register(Task)
admin.site.register(Comment)
