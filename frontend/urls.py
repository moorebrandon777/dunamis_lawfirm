from django.urls import path
from . import views 

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('robots.txt', views.robots_txt, name='robots'),

    path('attorneys/', views.attorneys_list, name='attorneys_list'),
    path('attorneys/<slug:slug>/', views.attorney_detail, name='attorney_detail'),
    path('services/', views.services_list, name='services_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
]