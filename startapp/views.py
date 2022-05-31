from genericpath import exists
from os import mkdir
from posixpath import dirname
from stat import FILE_ATTRIBUTE_DIRECTORY
from django.http import HttpRequest
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from boto.ec2 import *

# Create your views here.
#

FILE_PATH_DIR = 'uploads'

# Index HTML page.
def index(request):
    
    return render(request, 'default.html')

# Upload HTML Page.
def upload(request: HttpRequest):
    # check if exist folder path, else not exist any one
    # then create one.
    if not exists(FILE_PATH_DIR):
        mkdir(FILE_PATH_DIR, FILE_ATTRIBUTE_DIRECTORY) # I dont no if FILE_ATTRIBUTE_DIRECTORY is correct ?
    else:
        pass # uses returns is an bad ideeded!
    
    # check it for me, 'POST' request in HTML form.
    # returns me page render with '{values:_fp'}
    if request.method == 'POST':
        request_files = request.FILES['document'] if 'document' in request.FILES else None
        if request_files:
            fp = FileSystemStorage()
            file_url = fp.url(FILE_PATH_DIR + '/' + request_files.name)
            file = fp.save(file_url, request_files)
        #return render(request, "upload.html", {"values":files})

    return render(request, "upload.html")