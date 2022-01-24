
from email import contentmanager
from pyexpat import model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView



from post_app.models import Post, Usuarios

# Create your views here.


class Post_addView(CreateView):
    model = Post
    fields = ['nombre', 'autor', 'contenido', 'visible']
    success_url =  reverse_lazy('post_app:post_list')
    
    
class Post_listView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    
class Usuarios_listView(ListView):
    model= Usuarios
    context_object_name= 'usuarios'
    template_name= 'usuarios_list.html'

class Usuarios_addView(CreateView):
    model= Usuarios
    fields= ['username', 'nombre_usuario','apellido_usuario', 'email', 'profesion', 'edad']
    success_url =  reverse_lazy('post_app:usuarios_list')
