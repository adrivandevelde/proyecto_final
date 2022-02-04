

from dataclasses import fields
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
#se importa inlineformset_factory para hacer el alta de un post con img en el mismo formularia
from django.forms.models import inlineformset_factory
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from post_app.models import Post, Usuarios, Temas, Image_Post
from post_app.forms import PostForm


ImagenFormset = inlineformset_factory(
    Post, Image_Post, fields=('img',)
)

# Create your views here.

#Queda decrpted hasta ver como hcerlo funcionar se crea una funcion custom
class Post_addView(CreateView):
    model = Post
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            print(self.request.FILES)
            data["imagen"] = ImagenFormset(self.request.POST, self.request.FILES)
        else:
            data["imagen"] = ImagenFormset()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        imagen = context["imagen"]
        self.object = form.save()
        if imagen.is_valid():
            imagen.instance = self.object
            print(imagen.instance)
            imagen.save()
        else:
            print("El formde imagenes no es valido")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_app:post_list')
    
    

    
        
#funcion custom para hacer el crate del post con imagenes en un solo form
"""
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


No logré hacerlo funcionar exploro otra opcion
def create_post(request):
    PostinlineFormSet = inlineformset_factory(
        Post, Image_Post, form=PostForm
        )
    
    if request.method == 'POST':
        image_PostForm = Image_PostForm(request.POST)
        
        if image_PostForm.is_valid():
            newImage = image_PostForm.save()
            postinlineFormSet = PostinlineFormSet(request.POST, request.FILES, instance=newImage)
            
            if postinlineFormSet.is_valid():
                postinlineFormSet.save()
                return HttpResponseRedirect(reverse_lazy('post_app:post_list'))
            else:
                postinlineFormSet = PostinlineFormSet(request.POST, request.FILES, instance=newImage)
        else:
            postinlineFormSet = PostinlineFormSet()
            postForm = PostForm()
    
        
    postinlineFormSet = PostinlineFormSet()
    print(postinlineFormSet)
    
    return render(request, 'post_app/post_form.html', {'form': postinlineFormSet})
            
   """         
        
        
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
    fields = ['nombre', 'autor', 'contenido', 'visible']
    
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered.
        # the difference with CreateView is that
        # on this view we pass instance argument
        # to the formset because we already have
        # the instance created
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            print("Es un Post")
            data["imagen"] = ImagenFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            print(self.object)
            data["iamgen"] = ImagenFormset(self.request.FILES, instance=self.object )
        return data

    def form_valid(self, form):
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
