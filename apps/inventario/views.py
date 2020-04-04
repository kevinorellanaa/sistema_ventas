from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView

# Create your views here.

class base_site(TemplateView):
    template_name='base_site.html'
