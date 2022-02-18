"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls import handler404, handler403
from .views import index,About, login_request, register, error_403_view, editar_perfil
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', About.as_view(), name='about'),
    path('post/', include('post_app.urls')),
    path('login', login_request, name='login'),
    path('register', register, name= 'register'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('user_edit', editar_perfil, name= 'user_editar'),
    
       
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })]


handler404 = 'blog.views.error_404_view'

handler403 = error_403_view