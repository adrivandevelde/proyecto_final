from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from blog.forms import UserRegisterForm, UserEditionForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from user.models import User
from .forms import ContactForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

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

@login_required
def editar_perfil(request):
    usuario= request.user
    if request.method == 'POST':
        formulario= UserEditionForm(request.POST)
        if formulario.is_valid():
            data= formulario.cleaned_data
            usuario.email = data['email']
            usuario.set_password(data['password1'])
            usuario.first_name= data['first_name']
            usuario.last_name= data['last_name']
            usuario.save()
            return redirect('post/')
    else:
        formulario= UserEditionForm({'email': usuario.email})
    return render (request, 'usuario_editar.html', {'form': formulario})

""" class Editar_usuario(UserPassesTestMixin, UpdateView):
    model = User
    login_url = 'login'
    raise_exception = False
    permission_denied_message = 'El Usuario Solo Puede Eliminar/Modificar sus propios datos'
    success_url = reverse_lazy('usuarios_list')
    fields = ['email', 'password1', 'first_name','last_name', 'web_personal'] """


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                print(f'asunto {subject}, desde {from_email}, mensaje {message}')
                send_mail(subject, message, from_email, ['agsbenitez@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})

class successView(TemplateView):
    template_name = "success.html"


