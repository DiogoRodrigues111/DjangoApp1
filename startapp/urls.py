'''
Created on May 23, 2022

@author: drroe
'''

from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('upload', views.upload),
] + static(settings.STATIC_CSS_URL, document_root=settings.STATIC_CSS_ROOT)