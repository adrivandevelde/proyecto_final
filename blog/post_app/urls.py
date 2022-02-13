from django.contrib import admin
from django.urls import path,re_path

from post_app.views import Post_Update, Post_addView, Post_DeleteView, Post_listView, Post_detailView, Post_sarch, Usuarios_listView, Temas_listView, Tema_addView, Tema_Update
from post_app.views import Tema_detailView, Tema_DeleteView, Error_delete

from django.conf.urls.static import static
#

app_name='post_app'

urlpatterns = [
    path('add', Post_addView.as_view(), name="post_add"),
    path('update/<pk>', Post_Update.as_view(), name="update" ),
    path("delete/<pk>", Post_DeleteView.as_view(), name="delete"),
    path('', Post_listView.as_view(), name="post_list"),
    path("detail/<pk>", Post_detailView.as_view(), name="detail"),
    path('usuarios/lista', Usuarios_listView.as_view(), name="usuarios_list"),
    #path('usuario/agregar', Usuarios_addView.as_view(), name="usuario_add"),
    path("tema/detail/<pk>", Tema_detailView.as_view(), name="tema_detail"),
    path('temas/lista', Temas_listView.as_view(), name="temas_list"),
    path("tema/update/<pk>", Tema_Update.as_view(), name="tema_update"),
    path('tema/agregar', Tema_addView.as_view(), name="tema_add"),
    path("tema/delete/<pk>", Tema_DeleteView.as_view(), name="tema_delete"),
    path("tema/error/", Error_delete.as_view(), name="error_delete"),
    path('search', Post_sarch.as_view(), name="search"),
    
]


