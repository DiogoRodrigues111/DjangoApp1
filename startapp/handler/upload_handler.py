from ..forms.forms import UploadFileClass

def register_file(_name, _f):
    with open (_name + _f, 'wb+') as dst:
        for _chunks in _f.chunks():
            dst.write(_chunks);