"""from dataclasses import fields
from django.forms import TextInput, Textarea, CheckboxInput,  ModelForm, ModelChoiceField, Form
from .models import Post, Image_Post, Temas


class PostForm(Form):
    model = Post
    nombre = TextInput()
    autor = TextInput()
    contenido = Textarea
    tema = ModelChoiceField(queryset=Temas.objects.all())
    visible = CheckboxInput()
    
    class Meta:
        model = Post
        #fields = '__all__'
        fields = [
            'nombre',
            'autor',
            'contenido',
            'tema',
            'visible'
        ]
    
        labels = {
            'nombre':'Nombre del Post',
            'autor': 'Autor del Post',
            'contenido': 'Contenido del Post',
            'tema':'Tema del Post',
            'visible': 'Visible',
        }

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'autor': TextInput(attrs={'class': 'form-control'}),
            'contenido': Textarea(attrs={'class':'form-control'}),
            'tema': ModelChoiceField(queryset=Temas.objects.all(), to_field_name=None) ,
            'visible': CheckboxInput(attrs={'class': 'form-control'})
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