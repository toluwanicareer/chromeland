from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

class Google(TemplateView):
    template_name = 'googlee294f3cea858d890.html'

class Yandex(TemplateView):
    template_name = 'yandex_e338a2b8290dc352.html'

class Sitemap(TemplateView):
    template_name = 'sitemap.xml'

class Robot(TemplateView):
    template_name = 'robots.txt'