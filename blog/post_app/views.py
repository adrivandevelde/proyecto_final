

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from post_app.models import Post, Usuarios, Temas, Image_Post
from post_app.forms import PostForm, Image_PostForm

# Create your views here.


class Post_addView(CreateView):
    
    model = Post
    form_class = PostForm
    seconf_form_class = Image_PostForm
    success_url =  reverse_lazy('post_app:post_list')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        context['form2'] = self.seconf_form_class(self.request.GET)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.imagen_post = form2.save()
            solicitud.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
        
class Post_listView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    
class Post_detailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_app/post_detail.html'
    

class Post_Update(UpdateView):
    model = Post
    fields = ['nombre', 'autor', 'contenido', 'visible', 'imagenes']
    template_name_suffix = '_update_form' 
    
     
    
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
