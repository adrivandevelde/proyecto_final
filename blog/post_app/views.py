
from email import contentmanager
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
<<<<<<< HEAD
from .models import Post



from post_app.models import Post, Usuarios
=======
from post_app.models import Post, Usuarios, Temas
>>>>>>> a0baf2e1fad321c6b5d18fe0a4b867900da9537d

# Create your views here.


class Post_addView(CreateView):
    model = Post
    fields = ['nombre', 'autor', 'contenido', 'visible']
    success_url =  reverse_lazy('post_app:post_list')
    
    
class Post_listView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    
class Post_sarch(ListView):
    template_name =  'post_list.html' #se indica el template a utiliza 
    #en este caso el queryset va a depender de lo que el snippets search nos mande en el atributo q
    #queryset =  
    

    def get_queryset(self):#se hace la consulta        
        filters = Q(nombre__icontains=self.query()) | Q(autor__icontains=self.query()) | Q(contenido__icontains=self.query())
        return Post.objects.filter(filters)   

    def query(self):#se obtiene el valor de q en el request
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs): #sobre esctibo el metodo para obtener el contexto de la peticion
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['posts'] = context['post_list']
        
        return context
    
    
    
class Usuarios_listView(ListView):
    model= Usuarios
    context_object_name= 'usuarios'
    template_name= 'usuarios_list.html'

class Usuarios_addView(CreateView):
    model= Usuarios
    fields= ['username', 'nombre_usuario','apellido_usuario', 'email', 'profesion', 'edad']
    success_url =  reverse_lazy('post_app:usuarios_list')

class Temas_listView(ListView):
    model= Temas
    context_object_name= 'temas'
    template_name= 'temas_list.html'

class Temas_addView(CreateView):
    model= Temas
    fields= ['categoria', 'descripcion']
    success_url =  reverse_lazy('post_app:temas_list')
