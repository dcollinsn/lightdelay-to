"""lightdelay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView

from lightdelay import views

urlpatterns = [
    path('about/',
         TemplateView.as_view(template_name="lightdelay/about.html"),
         name='about'),
    path('docs/',
         TemplateView.as_view(template_name="lightdelay/docs.html"),
         name='docs'),
    path('sitemap.xml',
         TemplateView.as_view(template_name="lightdelay/sitemap.xml"),
         name='sitemap'),
    path('',
         views.lightdelay_0arg,
         name='lightdelay_0arg'),
    path('<str:query>',
         views.lightdelay_1arg,
         name='lightdelay_1arg'),
    path('<str:query>/',
         views.lightdelay_1arg,
         name='lightdelay_1arg'),
    path('<str:query1>/<str:query2>',
         views.lightdelay_2arg,
         name='lightdelay_2arg'),
    path('<str:query1>/<str:query2>/',
         views.lightdelay_2arg,
         name='lightdelay_2arg'),
    path('<str:query1>/<str:query2>/<str:query3>',
         views.lightdelay_3arg,
         name='lightdelay_3arg'),
    path('<str:query1>/<str:query2>/<str:query3>/',
         views.lightdelay_3arg,
         name='lightdelay_3arg'),
]
