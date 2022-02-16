from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from blog.forms import UserRegisterForm
from django.views.generic import TemplateView

def index(request):
    return redirect('post_app:post_list')


class About(TemplateView):
    template_name = "about.html"
    
    
def error_404_view(request, exception):
    data = {"name": "GrupoD"}
    return render(request,'error_404.html', data)

def error_403_view(request, exception):
    return render(request, 'error_403.html', {'exception': exception})
    

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            usuario= form.cleaned_data['username']
            contrasena= form.cleaned_data['password']
            user= authenticate(username=usuario, password=contrasena)

            if user is not None:
                login(request, user)
                return redirect('post/')
            else:
                return render(request, 'login.html', 
                {'form': form, 'error':'No es válido el usuario y/o la contraseña'})

        else:
            return render(request, 'login.html', {'form': form, 'error':'No es válido el usuario y/o la contraseña'})
    else:
        form = AuthenticationForm()
        return render (request, 'login.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return HttpResponse(f'Usuario {username} creado correctamente!')
        else:
            return render(request, 'registro.html', {'form': form, 'error':'algunos campos tienen errores'})
            
    else:
            form = UserRegisterForm()
    return render (request, 'registro.html', {'form': form})
