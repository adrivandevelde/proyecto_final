
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, CharField, PasswordInput, TextInput
from django import forms


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



class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Su email", required=True)
    subject = forms.CharField(label="Asunto", required=True)
    message = forms.CharField(label="Mensaje", widget=forms.Textarea, required=True)
    
    
