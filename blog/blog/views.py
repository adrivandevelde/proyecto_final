


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

def index(request):
    return redirect('post_app:post_list')


class About(TemplateView):
    template_name = "about.html"
