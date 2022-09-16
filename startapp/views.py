from genericpath import exists
from os import mkdir, listdir
from django.http import HttpRequest
from django.shortcuts import render
from .forms.forms import UploadFileClass
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect

def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        render: Django library
    """

    if not exists("media/"):
        mkdir("media/")

    for foreach in listdir("media/"):
        print (f'Files Founds: {foreach}')
        
        jpg = foreach.endswith('.jpg')
        videos = foreach.endswith('.mp4')

        sequence = 'media/'
        _lst_itr = sequence.join(foreach)

        media_static = {
            'jpg':jpg,
            'videos':videos,
            'listdir':_lst_itr
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
            return redirect('/')
    else:
        form = UploadFileClass()
        print ('Form returns new instance or not valid.')

    return render(request, 'upload.html', {'form':form})