from genericpath import exists
from django.http import HttpRequest
from django.shortcuts import render
from .handler.upload_handler import register_file
from .forms.forms import UploadFileClass


def index(request):
    """
    Generating HTML Index page results.
    
    Returns:
        render: Django library
    """
    return render(request, 'default.html')


def upload(request: HttpRequest):
    """
    Generating HTML Upload page results.
    
    Args:
        request (HttpRequest): Get File to upload system.

    Returns:
        render: Django library
    """
    form = UploadFileClass(request.POST, request.FILES['file'])
    if form.is_valid:
        register_file('hasuh.jpg', request.FILES)
        if exists('media/hasuh.jpg'):
            print ('Upload complete with success')
    else:
        form = UploadFileClass()
        print ('Form returns new instance or not valid.')
        pass # returns nothing, and continue with next.
    return render(request, "upload.html", {'form':form})