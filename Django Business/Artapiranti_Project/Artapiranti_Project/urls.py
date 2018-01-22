"""Artapiranti_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from Artapiranti.views import Admin,Login,Logout,Validcode,Product,Staff,Blog,ContactUs,Copyright,Parter,TimeLine,Test
urlpatterns = [
    path('admin/', Admin.as_view(),name='admin'),
    path('login/', Login.as_view(),name='login'),
    path('logout/', Logout.as_view(),name='logout'),
    path('validcode/', Validcode.as_view(),name='validcode'),
    path('product/', Product.as_view(),name='product'),
    path('staff/', Staff.as_view(),name='staff'),
    path('blog/', Blog.as_view(),name='blog'),
    path('parter/', Parter.as_view(),name='parter'),
    path('timeline/', TimeLine.as_view(),name='timeline'),
    path('contactus/', ContactUs.as_view(),name='contactus'),
    path('copyright/', Copyright.as_view(),name='copyright'),
    path('test/', Test.as_view(),name='test'),
]
