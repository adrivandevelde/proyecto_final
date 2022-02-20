
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your models here.


class Post(models.Model):
    nombre = models.CharField("Titulo", max_length=50, blank=False)
    #autor = models.CharField("Autor", max_length=50, blank=False)
    autor = models.ForeignKey(User, verbose_name="Autor", on_delete=models.SET_NULL, related_name="nombreAutor", null=True, blank=True)
    contenido = models.TextField("Contenido", blank=True)
    fecha_publicacion = models.DateTimeField("Fecha de Publicación", auto_now_add=True)
    #fecha_ultima_modificacion = models.DateTimeField("Fecha de Publicaión", blank=True)
    visible = models.BooleanField()
    tema = models.ForeignKey("Temas", verbose_name="Tema", on_delete=models.PROTECT, related_name="tema", blank=True, null=True)
    #imagen = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.nombre
    
#Esta función me permite crear una sub carpeta dento de la estructira de archivs con el id de post    
def post_image_paht(instance, filename):
    return 'post_{0}/{1}'.format(instance.post.id, filename)
    
class Image_Post(models.Model):
    post = models.ForeignKey("Post", verbose_name="Post", on_delete=models.RESTRICT, related_name="imagenes")
    img = models.ImageField("Imagen", upload_to=post_image_paht)
    
    def __str__(self):
        return str(self.post)
    
    class Meta:
        verbose_name = "Imagenes Post"
        
        
"""class Usuarios(models.Model):
    username=models.CharField(max_length=30)
    nombre_usuario= models.CharField(max_length=30)
    apellido_usuario= models.CharField(max_length=30)
    email= models.EmailField()
    profesion = models.CharField(max_length=30)
    edad= models.DecimalField(decimal_places= 0, max_digits= 3)
"""

class Temas(models.Model):
    categoria= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=30)

    
    def __str__(self):
        return self.categoria + ": " +self.descripcion