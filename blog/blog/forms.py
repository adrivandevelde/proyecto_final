
from turtle import textinput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, CharField, PasswordInput, TextInput


class UserRegisterForm(UserCreationForm):
    email= EmailField()
    password1= CharField(label='Contraseña', widget=PasswordInput)
    password2= CharField(label='Repetir contraseña', widget=PasswordInput)

    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2', 'last_name', 'first_name']
        help_texts= {k: '' for k in fields}
        
class UserEditionForm(UserCreationForm):
    email= EmailField()
    password1= CharField(label='Contraseña', widget=PasswordInput)
    password2= CharField(label='Repetir contraseña', widget=PasswordInput)
    
    class Meta:
        model= User
        fields= ['email', 'password1', 'password2', 'last_name', 'first_name']
        help_texts= {k: '' for k in fields}

