from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vulnerable/', include('vulnerable_app.urls')),
    path('secure/', include('secure_app.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
