from genericpath import exists
from os import mkdir
from django.http import HttpRequest
from django.shortcuts import render
from .handler.upload_handler import FileImporterSystem
from .forms.forms import UploadFileClass


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        render: Django library
    """
    if not exists("media/"):
        mkdir("media/")

    if request.method == 'POST':
        form = UploadFileClass(request.POST, request.FILES)
        if form.is_valid():
            for itname in request.FILES:
                FileImporterSystem.register_file("media/" + itname.name, request.FILES)
            print ('Upload complete with success')
    else:
        form = UploadFileClass()
        print ('Form returns new instance or not valid.')

    return render(request, 'default.html', {'form':form})


def upload(request: HttpRequest):
    """
    Generating HTML Upload page results.

    Args:
        request (HttpRequest): Get File to upload system.

    Returns:
        render: Django library
    """

    return render(request, "upload.html")#{'form':form}