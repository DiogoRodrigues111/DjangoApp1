from genericpath import exists
from os import mkdir, listdir, path
from django.http import HttpRequest
from django.shortcuts import render
from .forms.forms import UploadFileClass
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .databases.mongodb import mongo_user_db
from .databases.postgresql import pg_user_db

""" GLOBALS """

# Video and Image, iterable with HTML.
global g_video, g_image

""" CONSTANT """

# Create an table.
PG_CREATE_TABLE = \
    'CREATE TABLE pgUserTab(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR, email VARCHAR, password VARCHAR);'


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        rendering page
    """

    # Context Iterations.
    global g_video, g_image

    if not exists("media/"):
        mkdir("media/")

    """ When entry in home page the database, is created automatically. """

    # MongoDB
    mongo_user_db.create_instance_new_database('mongo_UserDB')
    # Postgres
    pg_user_db.create_new_cmd_pg(PG_CREATE_TABLE)

    # Take list of the files in media folder.
    foreach_media_folder = listdir('media/')

    # Make list of 'media/' folder for iterable with files.
    for lst in foreach_media_folder:

        """
        
        Only locking in JPG and MP4.
        Record values of the variable for print in Context.
        And take something value of the 'lst' iterator.
        
        """

        # Take values of the paths iterating.
        base = path.basename(lst)

        # The base is always > than one.
        if base.count(lst) > 0:
            # Iterable with JPG files.
            if base.endswith('.jpg'):
                image_source = base.split()
                g_image = base.format(*image_source).split()

            # Iterable with MP4 files.
            if base.endswith('.mp4'):
                video_source = base.split()
                g_video = base.format(*video_source).split()
        else:
            # Return then ...
            g_image = base.split()
            g_video = base.split()

    # Page Context.
    context_for_media = {
        'images': g_image,
        'videos': g_video,
    }

    return render(request, 'default.html', context_for_media)


def upload(request: HttpRequest):
    """
    Generating HTML Upload page results.

    Args:
        request (HttpRequest): Get File to upload system.

    Returns:
        rendering page.
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


def update(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    return render(request, 'update.html')


def signin(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    return render(request, 'signin.html')


def login(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    return render(request, 'login.html')
