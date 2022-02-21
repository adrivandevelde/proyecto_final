from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from user.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.deletion import ProtectedError
#se importa inlineformset_factory para hacer el alta de un post con img en el mismo formularia
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic  import TemplateView
from django.views.generic import DetailView
from django.views.generic.list import ListView

from post_app.models import Post, Temas, Image_Post






"""
Se crea el formulario de Post junto a de imágenes
"""
ImagenFormset = inlineformset_factory(
    Post, Image_Post, fields=('img',)
)

    
#https://swapps.com/es/blog/trabajando-con-formularios-anidados-con-django/

class Post_addView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Post
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
    """
    Post List: lista los post Visibles ordenados por fecha de manera Descendente

    Args:
        ListView (_type_): _description_
    """
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.filter(visible=True).order_by('-fecha_publicacion')
    allow_empty = True
    template_name = 'post_list.html'
    paginate_by = 5 
    
class Post_detailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_app/post_detail.html'
    

class Post_Update(UserPassesTestMixin, UpdateView):
    """
    Post Update

    Args:
        UserPassesTestMixin (_type_): Mixim para generar el control de usuario
        UpdateView (_type_):

    Raises:
        PermissionDenied: Si usuario no está logueado (lo redirige al login) o si no es el dueño del post (Mensaje de error)

    Returns:
        _type_: Edición del post
    """
    model = Post
    login_url = 'login'
    raise_exception = False
    permission_denied_message = 'El Usuario Solo Puede Eliminar/Modificar sus Propios Post'
    success_url = reverse_lazy('post_list')
    fields = ['nombre', 'contenido', 'visible', 'tema']
    
    
    def test_func(self):
        """metodo incorporado en UserPassesTestMixin
        se sobre escribe para hacer el control si el user es el credor del Post

        Returns:
            _type_: True / False
        """
        elPost = Post.objects.get(pk=self.kwargs.get('pk'))
        return (True if self.request.user.id == elPost.autor.id else False)
    
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
        
         
    def get_context_data(self, **kwargs):
        """redefinición del método
        necesario para insertar las imágenes que envía el formulario de imágenes del inLineFormSets 

        Returns:
            _type_: _description_
        """
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
    
class Post_DeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    login_url = 'login'
    success_url = reverse_lazy('post_app:post_list')
    permission_denied_message = 'El Usuario Solo Puede Eliminar/Modificar sus Propios Post'
    
        
    def test_func(self):
        """metodo incorporado en UserPassesTestMixin
        se sobre escribe para hacer el control si el user es el credor del Post

        Returns:
            _type_: True / False
        """
        elPost = Post.objects.get(pk=self.kwargs.get('pk'))
        return (True if self.request.user.id == elPost.autor.id else False)
    
    def handle_no_permission(self):
        """metodo incorporado en UserPassesTestMixin
        se sobre escribe para hacer el control si el user es el credor del Post

        Raises:
            PermissionDenied: si test_func devuelve False Genera el error de Permiso denegado

        Returns:
            _type_: _description_
        """
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
     
    
class Post_sarch(ListView):
    template_name =  'post_list.html' #se indica el template a utiliza 
    #en este caso el queryset va a depender de lo que el snippets search nos mande en el atributo q
    

    def get_queryset(self):#se hace la consulta        
        filters = Q(nombre__icontains=self.query()) | Q(autor__username__icontains=self.query()) | Q(contenido__icontains=self.query())
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


class Tema_addView(PermissionRequiredMixin, CreateView):
    model= Temas
    fields= ['categoria', 'descripcion']
    success_url =  reverse_lazy('post_app:temas_list')
    permission_required = 'post_app.add_tema'
    permission_denied_message = "Unicamente Administradores pueden Editar Temas"


class Tema_Update(PermissionRequiredMixin, UpdateView):
    model= Temas
    fields= ['categoria', 'descripcion']
    success_url =  reverse_lazy('post_app:temas_list')
    permission_required = 'post_app.change_tema'
    permission_denied_message = "Unicamente Administradores pueden Editar Temas"   


class Error_delete(TemplateView):
    template_name = "post_app/error_delete.html"


class Tema_DeleteView(PermissionRequiredMixin, DeleteView):
    model = Temas
    success_url = reverse_lazy('post_app:temas_list')
    permission_required = 'post_app.delete_tema'
    permission_denied_message = "Unicamente Administradores pueden Borrar Temas"
    
   
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.error(request,"No se puede borrar el tema ya que está siendo usado en otros Post")
            return redirect('post_app:error_delete') 

        return HttpResponseRedirect(success_url)
    
    