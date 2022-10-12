from http import cookies, client
from http.cookiejar import Cookie
from urllib import response
from urllib.request import HTTPCookieProcessor
from django import http
from django.http.cookie import SimpleCookie
from django.http import HttpResponse

class CookiesRecord:
    
    def cookies_new(response: HttpResponse):
        
        response.set_cookie("WebAppV1_Key", "WebApp v1 Diogo R Roessler", domain="WebSiteDjango_DiogoRRoessler")

        if response is not None:
            print(F"Cookies Created with successful with name of: {response}")

        return response