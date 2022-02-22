from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from blog.forms import UserRegisterForm, UserEditionForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test

from user.models import User
from .forms import ContactForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
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

"""
def user_test(request):
    summary

    Args:
        user (type): test para validar que el usuario logueado pueda editar solo su usario

    Returns:
        type: description
    
    print(request)
    eluser = User.objects.get(pk=request.kwargs.get('pk'))
    if eluser.is_superuser:
        return True
    else:
        return (True if self.request.user.id == eluser.autor.id else False)

@user_passes_test(user_test)
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
"""
class editar_perfil(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserEditionForm
    template_name = 'usuario_editar.html' 
    success_url =  reverse_lazy('post_app:usuarios_list')
    permission_required = 'post_app.change_user'
    permission_denied_message = "Unicamente Administradores pueden Editar Usuarios"
    
    
    def test_func(self):
        """metodo incorporado en UserPassesTestMixin
        se sobre escribe para hacer el control si el user es el credor del Post

        Returns:
            _type_: True / False
        """
        eluser = User.objects.get(pk=self.kwargs.get('pk'))
        return (True if self.request.user.id == eluser.id else False)
    
    def handle_no_permission(self):
        """metodo incorporado en UserPassesTestMixin
        se sobre escribe para hacer el control si el user es el credor del Post

        Raises:
            PermissionDenied: si test_func devulve False Genera el error de Permiso denegado

        Returns:
            _type_: _description_
        """
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class User_detailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'post_app/user_detail.html'
    
class Usuarios_listView(ListView):
    model= User
    context_object_name= 'usuarios'
    template_name= 'usuarios_list.html'

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


