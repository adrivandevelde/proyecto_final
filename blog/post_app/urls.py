from django.contrib import admin
from django.urls import path
from post_app.views import Post_addView, Post_listView

app_name='post_app'

urlpatterns = [
    path('add', Post_addView.as_view(), name="post_add"),
    path('', Post_listView.as_view(), name="post_list")
    
]
