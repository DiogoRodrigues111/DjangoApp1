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

    # Iteratives paths
    #path('', include('../../../../media/'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 