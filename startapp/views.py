from genericpath import exists
from os import mkdir, listdir, path
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms.forms import(
     PgBanned
     , UploadFileClass
     , PgSignInRegister
     , PgUpdate
     , PgDelete
     , PgUnbanned
)
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .databases.mongodb import mongo_user_db
from .databases.postgresql import pg_user_db
from .cookies.cookies_rec import CookiesRecord
from django.utils.datastructures import MultiValueDictKeyError

""" GLOBALS """

# Video and Image, iterable with HTML.
global g_video, g_image
global register, delete_user, update_user, banned_user, desbanned

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
    global g_video, g_image

    if not exists("media/"):
        mkdir("media/")

    if not exists("media/videos/"):
        mkdir("media/videos/")

    if not exists("media/images/"):
        mkdir("media/images/")

    """ When entry in home page the database, is created automatically. """

    # Cookies
    CookiesRecord.cookies_new(response=HttpResponse("Cookies Created!"))

    # MongoDB
    mongo_user_db.create_instance_new_database('mongo_UserDB', "User_Collect")

    # Postgres
    pg_user_db.create_new_cmd_pg(PG_CREATE_TABLE)

    """ Create a iteration with HTML for the media folder. """

    # Take list of the files in media folder.
    foreach_media_videos = listdir("media/videos/")
    foreach_media_images = listdir("media/images/")

    g_image = {}
    g_video = {}

    # Make list of 'media/' folder for iterable with files.
    for lst_img in foreach_media_images:

        """
        
        Only locking in JPG.
        Record values of the variable for print in Context.
        And take something value of the 'lst' iterator.
        
        """

        # Take values of the paths iterating.
        base = path.basename(lst_img)

        # The base is always > than one.
        if base.count(lst_img) > 0:
            # Iterable with JPG files.
            g_image = base.split()


    # Make list of 'media/' folder for iterable with files.
    for lst_vd in foreach_media_videos:

        """
        
        Only locking in MP4.
        Record values of the variable for print in Context.
        And take something value of the 'lst' iterator.
        
        """

        # Take values of the paths iterating.
        base = path.basename(lst_vd)

        if base.count(lst_vd) > 0:
            # Iterable with MP4 files.
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

    Entry in this page for only banned user.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    """ If you stay in this page, then it is for banned some user. """

    global banned_user

    banned_user = PgBanned(request.POST)

    if request.method == 'POST':

        email = request.POST['email']

        # Result is always true.
        # This checking only work if stay checked.
        banned = request.POST['bool_banned']

        pg_user_db.pg_user_banned(banned, email)

        if banned_user.is_valid():
            print(F'User Banned with success with values: Email = {email} Banned: {banned}')
            redirect('/')
        else:
            raise RuntimeError(F'Failed to BANNING user. with Email: {email}. Check right email digited.')

    # Context Register Data
    user_banned_context = {
        'user_banned_data': banned_user,
    }

    return render(request, 'banned.html', user_banned_context)


def unbanned(request: HttpRequest):
    """
    
    Generating HTML Update page results.

    Entry in this page for only unbanned user.

    Args:
        request: Results requests.

    Returns:
        rendering page.

    """

    global desbanned

    desbanned = PgUnbanned(request.POST)

    if request.method == 'POST':

        email = request.POST['email']

        # Result is always true.
        # This checking only work if stay checked.
        banned = request.POST['bool_banned'] if not True else False or False

        pg_user_db.pg_user_banned(banned, email)

        if desbanned.is_valid():
            print(F'User UnBanned with success with values: Email = {email} Banned: {banned}')
            redirect('/')
        else:
            raise RuntimeError(F'Failed to Unbanning user. with Email: {email}. Check right email digited.')

    # Context Register Data
    user_banned_context = {
        'unbanned_data': desbanned,
    }

    return render(request, 'unbanned.html', user_banned_context)