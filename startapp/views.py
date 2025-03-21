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

    global value_image
    global value_video

    if not exists("media/"):
        mkdir("media/")

    # Images
    images = listdir('media/')
    for lst_image in images:
        if lst_image.endswith('.jpg'):
            value_image = path.basename(lst_image)
            print(f'JPG IMAGES ONLY FOUND: {value_image}')

    # Videos
    videos = listdir('media/')
    for lst_video in videos:
        if lst_video.endswith('.mp4'):
            value_video = path.basename(lst_video)
            print(f'MP4 VIDEOS ONLY FOUND {value_video}')

    media_static = {
        'images': value_image,
        'videos': value_video
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
