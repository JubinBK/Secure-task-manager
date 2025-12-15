from django.contrib import admin
from .models import SecureTask, SecureComment

admin.site.register(SecureTask)
admin.site.register(SecureComment)
