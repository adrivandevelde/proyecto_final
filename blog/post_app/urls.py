from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from post_app.views import Post_addView, Post_listView, Post_sarch, Usuarios_listView, Usuarios_addView
=======
from post_app.views import Post_addView, Post_listView, Post_sarch, Usuarios_listView, Usuarios_addView, Temas_addView, Temas_listView
>>>>>>> a0baf2e1fad321c6b5d18fe0a4b867900da9537d

app_name='post_app'

urlpatterns = [
    path('add', Post_addView.as_view(), name="post_add"),
    path('', Post_listView.as_view(), name="post_list"),
    path('lista_usuarios', Usuarios_listView.as_view(), name="usuarios_list"),
    path('agregar_usuario', Usuarios_addView.as_view(), name="usuario_add"),
<<<<<<< HEAD
=======
    path('lista_temas', Temas_listView.as_view(), name="temas_list"),
    path('agregar_temas', Temas_addView.as_view(), name="tema_add"),
>>>>>>> a0baf2e1fad321c6b5d18fe0a4b867900da9537d
    path('search', Post_sarch.as_view(), name="search")
    
]
