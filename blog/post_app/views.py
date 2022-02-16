from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic  import TemplateView
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
#se importa inlineformset_factory para hacer el alta de un post con img en el mismo formularia
from django.forms.models import inlineformset_factory
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from post_app.models import Post, Temas, Image_Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


from django.contrib.auth.models import User




ImagenFormset = inlineformset_factory(
    Post, Image_Post, fields=('img',)
)

    
#https://swapps.com/es/blog/trabajando-con-formularios-anidados-con-django/

class Post_addView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    #redirect_field_name = 'post/post_add'
    model = Post
    #form_class = PostForm
    fields = ['nombre', 'contenido', 'visible', 'tema']
    
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["imagen"] = ImagenFormset(self.request.POST, self.request.FILES)
        else:
            data["imagen"] = ImagenFormset()
        return data
    
    def form_valid(self, form):
        #se toma el usuario activo para pasarlo a la tabla como creador del post
        owner = self.request.user
        #se instancia el campo con el usuario activo
        form.instance.autor = owner
        context = self.get_context_data()
        imagen = context["imagen"]
        self.object = form.save()
        if imagen.is_valid():
            imagen.instance = self.object
            imagen.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_app:post_list')
    
    
        
class Post_listView(ListView):
    
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    
class Post_detailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_app/post_detail.html'
    

class Post_Update(UserPassesTestMixin, UpdateView):
    model = Post
    login_url = 'login'
    raise_exception = False
    permission_denied_message = 'El Usuario Solo Puede Eliminar/Modificar sus Propios Post'
    success_url = reverse_lazy('post_list')
    fields = ['nombre', 'contenido', 'visible', 'tema']
    
    
    def test_func(self):
        elPost = Post.objects.get(pk=self.kwargs.get('pk'))
        return (True if self.request.user.id == elPost.autor.id else False)
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        
    
     
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["imagen"] = ImagenFormset(self.request.POST,self.request.FILES, instance=self.object)
        else:
            data["imagen"] = ImagenFormset(instance=self.object )
        return data

    def form_valid(self, form):
        owner = self.request.user
        #se instancia el campo con el usuario activo
        form.instance.autor = owner
        context = self.get_context_data()
        children = context["imagen"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_app:post_list')
    
class Post_DeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_app:post_list')
    
     
    
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
    model= User
    context_object_name= 'usuarios'
    template_name= 'usuarios_list.html'


class Temas_listView(ListView):
    model= Temas
    context_object_name= 'temas'
    template_name= 'temas_list.html'
    
class Tema_detailView(DetailView):
    model = Temas
    context_object_name = 'tema'
    template_name = 'post_app/tema_detail.html'

class Tema_addView(CreateView):
    model= Temas
    fields= ['categoria', 'descripcion']
    success_url =  reverse_lazy('post_app:temas_list')

class Tema_Update(UpdateView):
    model= Temas
    fields= ['categoria', 'descripcion']
    success_url =  reverse_lazy('post_app:temas_list')
    
class Error_delete(TemplateView):
    template_name = "post_app/error_delete.html"

class Tema_DeleteView(DeleteView):
    model = Temas
    success_url = reverse_lazy('post_app:temas_list')
    
   
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.error(request,"No se puede borrar el tema ya que está siendo usado en otros Post")
            return redirect('post_app:error_delete') # The url of the delete view (or whatever you want)

        return HttpResponseRedirect(success_url)