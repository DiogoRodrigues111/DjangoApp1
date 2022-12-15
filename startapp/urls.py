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
    path('update', views.update),
    path('signin', views.signin),
    path('login', views.login),
    path('delete', views.delete),
    path('banned', views.banned),
    path('unbanned', views.unbanned),
    #path('mail', views.send_email),
    path('success', views.success),
    path('failed', views.failed)
] + static(settings.STATIC_CSS_URL, document_root=settings.STATIC_CSS_ROOT)