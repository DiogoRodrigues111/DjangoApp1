
from genericpath import exists
from os import mkdir
from django.http import HttpRequest


class FileImporterSystem:
    def check_media_folder(folder) -> bool:
        if exists(folder):
            pass
        return True

    def register_file(__path, __r: HttpRequest):
        with open (__path, 'wb+') as dst:
            for it in __r.FILES:
                dst.write(it['file'])