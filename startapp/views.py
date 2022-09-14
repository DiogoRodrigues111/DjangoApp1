from genericpath import exists
from os import mkdir, listdir
from urllib import response
from urllib.request import url2pathname
from django.http import HttpRequest
from django.shortcuts import render
from .handler.upload_handler import FileImporterSystem
from .forms.forms import UploadFileClass
from django.core.files.storage import FileSystemStorage
from io import FileIO


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        render: Django library
    """

    if not exists("media/"):
        mkdir("media/")

    files = listdir("media/")

    for foreach in files:
        print (f"Files Found: {foreach}")
        
        media_static = {
            'media_source':url2pathname(foreach)
        }

    return render(request, 'default.html', media_static)


def upload(request: HttpRequest):
    """
    Generating HTML Upload page results.

    Args:
        request (HttpRequest): Get File to upload system.

    Returns:
        render: Django library
    """

    if request.method == 'POST':
        form = UploadFileClass(request.POST, request.FILES)
        file_upload = request.FILES['file']
        fs = FileSystemStorage()
        file_name = fs.save(file_upload.name, file_upload)
        fs.url(file_name) # test without this
        if form.is_valid():
            print ('Upload complete with success')
    else:
        form = UploadFileClass()
        print ('Form returns new instance or not valid.')

    return render(request, 'upload.html', {'form':form})