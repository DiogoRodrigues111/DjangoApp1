from genericpath import exists
from os import mkdir, listdir, path
from django.http import HttpRequest
from django.shortcuts import render
from .forms.forms import UploadFileClass
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .databases.mongodb import user_db


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        rendering page
    """

    global value_image
    global value_video
    global cxt_media

    if not exists("media/"):
        mkdir("media/")

    # When entry in home page the MongoDB database, is created automatically.
    user_db.create_instance_new_database('mongo_UserDB')

    # Images
    # Get iterator of the media folder.
    images = listdir('media/')
    for lst_image in images:
        filenames_ends = lst_image.endswith('.jpg')
        if filenames_ends:
            # Lock only in JPG.
            # Record values of the variable for print in Context.
            # And take something value of the 'List_Image'.
            value_image = path.basename(lst_image)
            # Fix this, foreach wrong
            cxt_media = {
                'images': value_image,
            }

    # Videos
    # Get iterator of the media folder.
    videos = listdir('media/')
    for lst_video in videos:
        if lst_video.endswith('.mp4'):
            # Lock only in MP4
            # Record values of the variable for print in Context.
            # And take something value of the 'list_video'
            value_video = path.basename(lst_video)
            # Fix this, foreach wrong
            cxt_media = {
                'videos': value_video,
            }

    return render(request, 'default.html', cxt_media)


def upload(request: HttpRequest):
    """
    Generating HTML Upload page results.

    Args:
        request (HttpRequest): Get File to upload system.

    Returns:
        rendering page
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
