
from genericpath import exists
from io import FileIO
from xmlrpc.client import Boolean


class FileImporterSystem:
    def check_media_folder(folder) -> bool:
        if exists(folder):
            pass
        return True

    def register_file(_name):
        with open (_name, 'w+') as dst:
            if check_media_folder('media/'):
                dst.write(_name)