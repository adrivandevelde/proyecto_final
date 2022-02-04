from dataclasses import fields
from django.forms import widgets, TextInput, Textarea, CheckboxInput, ImageField, ModelForm
from .models import Post, Image_Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        """fields = [
            'nombre',
            'autor',
            'contenido',
            'visible'
        ]
    
        labels = {
            'nombre':'Nombre',
            'autor': 'Autor',
            'contenido': 'Contenido del Post',
            'visible': 'Visible',
        }

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'autor': TextInput(attrs={'class': 'form-control'}),
            'contenido': Textarea(attrs={'class':'form-control'}),
            'visible':  CheckboxInput(attrs={'class':'form-control'})
        }"""
    
    
    
"""class Image_PostForm(ModelForm):
    class Meta:
        model = Image_Post
        exclude = ['post',]
        
        
        labels = {
            'img':'Imagen'
        }
        
        widgets = {
            'img': ImageField(),
        }"""