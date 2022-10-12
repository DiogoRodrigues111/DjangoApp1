from genericpath import exists
from http import cookies
from logging.config import valid_ident
from os import mkdir, listdir, path
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from urllib3 import HTTPResponse
from .forms.forms import PgBanned, UploadFileClass, PgSignInRegister, PgUpdate, PgDelete
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .databases.mongodb import mongo_user_db
from .databases.postgresql import pg_user_db
from .cookies.cookies_rec import CookiesRecord
from django.utils.datastructures import MultiValueDictKeyError

""" GLOBALS """

# Video and Image, iterable with HTML.
global g_video, g_image, video, images
global register, delete_user, update_user, banned_user

""" CONSTANT """

# Create a table in Postgres.
# TODO:
#  Possible change location.
PG_CREATE_TABLE = \
    'CREATE TABLE pgUserTab(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(50), email VARCHAR(50), password VARCHAR(50), is_banned BOOLEAN);'


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

    # Cookies
    CookiesRecord.cookies_new(response=HttpResponse("Cookies Created!"))

    # MongoDB
    mongo_user_db.create_instance_new_database('mongo_UserDB')
    # Postgres
    pg_user_db.create_new_cmd_pg(PG_CREATE_TABLE)

    """ Create a iteration with HTML for the media folder. """

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

    update_user = PgUpdate(request.POST)

    if request.method == 'POST':

        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']

        pg_user_db.update_new_table_pg(name, password, email)

        if update_user.is_valid():
            print(F'Data Updated: Name = {name}, Email = {email}, Password = {password}')
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

    register = PgSignInRegister(request.POST)

    if request.method == 'POST':

        """ HINTS: pgusertab.name email password """

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        banned = None

        try:
            banned = request.POST['bool_banned'] if banned is not True else False
        except MultiValueDictKeyError:
            pass

        pg_user_db.insert_new_data_pg(name, email, password, banned)

        if register.is_valid():
            print(F'Data Added: Name = {name}, Email = {email}, Password = {password}, Banned: {banned}')
            redirect('/')
        else:
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

    delete_user = PgDelete(request.POST)

    if request.method == 'POST':

        email = request.POST['email']

        pg_user_db.pg_delete_columns(email)

        if delete_user.is_valid():
            print(F'User Deleted with success with values: Email = {email}')
            redirect('/')
        else:
            raise RuntimeError('Failed to DELETE user')

    # Context Register Data
    delete_data_context = {
        'delete_data': delete_user,
    }

    return render(request, 'delete.html', delete_data_context)

def banned(request: HttpRequest):
    """

    Generating HTML Update page results.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    global banned_user

    banned_user = PgBanned(request.POST)

    if request.method == 'POST':

        email = request.POST['email']
        banned = request.POST['bool_banned']

        pg_user_db.pg_user_banned(banned, email)

        if banned_user.is_valid():
            print(F'User User Banned with success with values: Email = {email} Banned: {banned}')
            redirect('/')
        else:
            raise RuntimeError('Failed to BANNING user.')

    # Context Register Data
    user_banned_context = {
        'user_banned_data': banned_user,
    }

    return render(request, 'delete.html',user_banned_context)