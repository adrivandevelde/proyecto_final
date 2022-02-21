from django.contrib import admin
from .models import Post, Image_Post


class Image_Post_admin(admin.TabularInline):
    model = Image_Post

class Post_admin(admin.ModelAdmin):
    list_display = ('__str__','fecha_publicacion')
    inlines = [
        Image_Post_admin
        ]
    

# Register your models here.
admin.site.register(Post, Post_admin)
#admin.site.register(Image_Post)