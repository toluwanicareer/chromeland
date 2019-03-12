from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('googlee294f3cea858d890.html', views.Google.as_view()),
    path('yandex_e338a2b8290dc352.html', views.Yandex.as_view()),
    path('sitemap.xml', views.Sitemap.as_view()),
    path('robots.txt', views.Robot.as_view()),
    path('converter/<str:slug>', views.ConverterDetail.as_view(), name='converter-detail'),
    path('convert', views.Convert.as_view(), name='convert')
]

