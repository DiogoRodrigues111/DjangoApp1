from genericpath import exists
from os import mkdir, listdir, path
from django.http import HttpRequest
from django.shortcuts import render
from .forms.forms import UploadFileClass, PgSignInRegister, PgUpdate, PgDelete
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .databases.mongodb import mongo_user_db
from .databases.postgresql import pg_user_db


""" GLOBALS """

# Video and Image, iterable with HTML.
global g_video, g_image, video, images
global register, delete_user, update_user

""" CONSTANT """

# Create a table in Postgres.
# TODO:
#  Possible change location.
PG_CREATE_TABLE = \
    'CREATE TABLE pgUserTab(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR, email VARCHAR, password VARCHAR);'


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        rendering page
    """

    # Context Iterations.
    global g_video, g_image, video, images

    if not exists("media/"):
        mkdir("media/")

    """ When entry in home page the database, is created automatically. """

    # MongoDB
    mongo_user_db.create_instance_new_database('mongo_UserDB')
    # Postgres
    pg_user_db.create_new_cmd_pg(PG_CREATE_TABLE)

    # Take list of the files in media folder.
    foreach_media_folder = listdir('media/')

    video = {'videos' if 'videos' is None else not None}
    images = {'images' if 'images' is None else not None}

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

            video = {
                'videos': g_video,
            }
            images = {
                'images': g_image,
            }

    # Page Context.
    context_for_media = {
        'images': images,
        'videos': video,
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
        request: Results requests

    Returns:
        rendering page.

    """

    global update_user

    if request.method == 'POST':
        update_user = PgUpdate(request.POST)

        name = register.fields['name']
        email = register.fields['email']
        password = register.fields['password']

        pg_user_db.insert_new_data_pg(name, email, password)

        if update_user.is_valid():
            print(F'Data Added: Name = {name}, Email = {email}, Password = {password}')
            redirect('/')
        else:
            raise RuntimeError('Failed to register user')

    # Context Register Data
    update_data_context = {
        'update_data': update_user,
    }

    return render(request, 'update.html', update_data_context)


def signin(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    global register

    register = PgSignInRegister()

    if request.method == 'POST':
        register = PgSignInRegister(request.POST)

        name = register.fields['name']
        email = register.fields['email']
        password = register.fields['password']

        pg_user_db.insert_new_data_pg(name, email, password)

        if register.is_valid():
            print(F'Data Added: Name = {name}, Email = {email}, Password = {password}')
            redirect('/')
        else:
            register = PgSignInRegister()
            raise RuntimeError('Failed to register user')

    # Context Register User Data
    register_data_context = {
        'register_data': register,
    }

    return render(request, 'signin.html', register_data_context)


def login(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    return render(request, 'login.html')


def delete(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    global delete_user

    if request.method == 'POST':
        delete_user = PgDelete(request.POST)
        email = register.fields['email']

        pg_user_db.pg_delete_columns(email)

        if delete_user.is_valid():
            print('Failed to Delete user')
            redirect('/')
        else:
            raise RuntimeError('Failed to DELETE user')

    # Context Register Data
    delete_data_context = {
        'delete_data': delete_user,
    }

    return render(request, 'update.html', delete_data_context)
