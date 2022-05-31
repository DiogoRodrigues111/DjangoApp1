'''
Created on May 23, 2022

@author: drroe
'''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('upload', views.upload),
]
