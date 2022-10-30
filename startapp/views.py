from genericpath import exists
from os import mkdir, listdir, path
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms.forms import (
    PgBanned
, UploadFileClass
, PgSignInRegister
, PgUpdate
, PgDelete
, PgUnbanned
, SendEmail
, Login
, CheckLogin
)
from django.core.files.storage import FileSystemStorage
from .databases.mongodb import mongo_user_db
from .databases.postgresql import pg_user_db
from .cookies.cookies_rec import CookiesRecord
from .mail import email
from django.utils.datastructures import MultiValueDictKeyError

# from .cloud.google import storage

""" GLOBALS """

# Video and Image, iterable with HTML.
global register, delete_user, update_user, banned_user, desbanned

""" CONSTANT """

# Create a table in Postgres.
# TODO:
#  Possible change location.
PG_CREATE_TABLE = \
    'CREATE TABLE pgUserTab' \
    '(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(50), email VARCHAR(50), password VARCHAR(50), is_banned BOOLEAN);'


def index(request: HttpRequest):
    """
    Generating HTML Index page results.

    Returns:
        rendering page
    """

    if not exists("media/"):
        mkdir("media/")

    """ When entry in home page the database, is created automatically. """

    # Cookies
    CookiesRecord.cookies_new(self=CookiesRecord(), response=HttpResponse("Cookies created with success"))

    """ Databases """

    # MongoDB
    mongo_user_db.create_instance_new_database('mongo_UserDB', "User_Collect")

    # Postgres
    pg_user_db.create_new_cmd_pg(PG_CREATE_TABLE)

    """ Google Cloud """

    # It made for creating Bucket for Storage
    # The billing account for the owning project is disabled in state absent.
    # It is necessary pay for uses that function.
    # storage.create_new_bucket_google_cloud("user-client")

    """ Create a iteration with HTML. """

    email_display = CheckLogin(request.GET)["email"].value()

    context_page = {
        "Videos": index_videos(),
        "Images": index_images(),
        "Login": email_display
    }

    return render(request, 'default.html', context_page)


def index_videos():
    """
    Generating HTML Index page results.

    It is an extended function.

    Returns:
        rendering page

    """

    # Take list of the files in media folder.
    foreach_media = listdir("media/")

    return [i for i in foreach_media if i.endswith(".mp4")]


def index_images():
    """
    Generating HTML Index page results.

    It is an extended function.

    Returns:
        rendering page
    """

    # Take list of the files in media folder.
    foreach_media = listdir("media/")

    return [i for i in foreach_media if i.endswith(".jpg")]


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

        """ HINTS: pgusertab.name email password. Names of the columns. """

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

    user_login = Login(request.POST)

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]

        pg_user_db.pg_user_login(email=email, password=password)

        if user_login.is_valid():
            # It is checked automatically if email exists.
            # Take name values of email digitized.
            #email_if_check = request.POST["email"]
            # Send to next page, in the case of default.html.
            #login_check(email_if_check)

            return redirect("/")
        else:
            raise RuntimeError("Login forms not valid.")

    login_status = {
        "login": user_login
    }

    return render(request, 'login.html', login_status)


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


def send_email(request: HttpRequest):
    """

    Send an email.

    Generation Html page.

    """

    snd = SendEmail(request.POST)

    if request.method == "POST":

        param_subject = request.POST["subject"]
        param_text = request.POST["text"]
        param_email_to = request.POST["_to"]
        param_email_from = request.POST["_from"]

        email.create_new_email(subject=param_subject, message=param_text,
                                _from=param_email_from, _to=param_email_to)

        if snd.is_valid():
            print(F'Email send with success to {param_email_to}')
            redirect('/')
        else:
            raise RuntimeError(F'Failed to send email.')

    email_sender = {
        "sender": snd
    }

    return render(request, 'mail.html', email_sender)


def success(request: HttpRequest):
    return render(request, 'success.html')


def failed(request: HttpRequest):
    return render(request, 'failed.html')
