from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Converter
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import requests
from django.core.files.storage import FileSystemStorage
import convertapi
import pdb
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class HomeView(ListView):
    model=Converter
    queryset = Converter.objects.all()
    context_object_name = 'converters'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context=super(HomeView,self).get_context_data(**kwargs)
        context['title']='PDF Converter - Convert PDF files for free online'
        context['description']='Convert PDF files with our Converter tool - a free online PDF converter. Convert Word to PDF, JPG to PDF, Excel to PDF, HTML to PDF, PNG to PDF, etc.'
        context['thumbnail']='word-to-pdf.png'
        return context

class ConverterDetail(DetailView):
    model=Converter
    context_object_name = 'converter'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context=super(ConverterDetail,self).get_context_data(**kwargs)
        context['more_tools']=Converter.objects.all().exclude(id=self.object.id)
        context['converters']=Converter.objects.all()
        context['title']='PDF Converter - Convert '+self.object.title+' file for free online'
        context['description']=self.object.description
        context['thumbnail']=self.object.image_file
        return context


@method_decorator(csrf_exempt, 'dispatch')
class Convert(View):


    def get(self, request, *args, **kwargs):
        file_url=request.GET.get('file_url')
        filename=request.GET.get('file_name')
        file_type = filename.split('.').pop()
        response=do_convert(file_url,file_type,filename,'dropbox')
        return JsonResponse(response)


    def post(self, request,*args, **kwargs):
        convertapi.api_secret = settings.API_SECRET
        file=request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_type=filename.split('.').pop()
        uploaded_file_url = fs.url(filename)
        res=do_convert(filename,file_type,filename,'dropzone')
        return JsonResponse(res)


def do_convert(file_url, file_type, file_name, medium):
    convertapi.api_secret = settings.API_SECRET
    #base_url='https://pdftools.projecttopics.org'
    base_directory = settings.MEDIA_ROOT
    try:
        if file_type == 'docx':
            converter = Converter.objects.filter(convert_from=file_type.strip())[0]
        else:
            converter = Converter.objects.get(convert_from=file_type.strip())

    except Converter.DoesNotExist:
        return {'status': 404, 'data': 'Resource not found'}
    #
    # TODO: change file url before upload
    if medium == 'dropzone':
        file_url = '%s/%s' %(base_directory, file_url)
    try:
        upload_io = convertapi.UploadIO(open(file_url, 'rb'))
        result = convertapi.convert('pdf', {'File': upload_io})
        file_url = result.file.url
        return {'status': 200, 'data': file_url}
    except:
        return {'status': 400, 'data': 'API ERROR'}


#C:\Users\tolu\PycharmProjects\pdfconverter\media\Diamond Bank and Access Bank - Outcome of Court Ordered  Shareholders meeting - final 2 (1).docx
class Google(TemplateView):
    template_name = 'googlee294f3cea858d890.html'

class Yandex(TemplateView):
    template_name = 'yandex_e338a2b8290dc352.html'

class Sitemap(TemplateView):
    template_name = 'sitemap.xml'

class Robot(TemplateView):
    template_name = 'robots.txt'