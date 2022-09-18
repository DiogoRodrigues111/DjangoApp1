from genericpath import exists
from os import mkdir, listdir, path
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

    g_base = listdir('media/')
    for base in g_base:
        print(f'Files Founds: {base}')
        base = path.basename(base).split()
        if g_base.count(base) > 1:
            g_base = base

    media_static = {
        'base': base,
        'g_base': g_base,
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

        # test without this
        fs.url(file_name)

        if form.is_valid():
            print('Upload complete with success')
            return redirect('/')
    else:
        form = UploadFileClass()
        print('Form returns new instance or not valid.')

    return render(request, 'upload.html', {'form': form})
