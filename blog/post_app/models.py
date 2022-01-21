
from django.db import models

# Create your models here.


class Post(models.Model):
    nombre = models.CharField("Titulo", max_length=50, blank=False)
    autor = models.CharField("Autor", max_length=50, blank=False)
    contenido = models.TextField("Contenido", blank=True)
    fecha_publicacion = models.DateTimeField("Fecha de Publicaión", auto_now_add=True)
    #fecha_ultima_modificacion = models.DateTimeField("Fecha de Publicaión", blank=True)
    visible = models.BooleanField()
    
    def __str__(self):
        return (f"Post {self().nombre} autoria de {self().autor}")