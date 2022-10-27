from django.http import HttpResponse


class CookiesRecord:

    @staticmethod
    def cookies_new(self, response: HttpResponse):
        response.set_cookie("WebAppV1_Key", "WebApp v1 Diogo R Roessler", domain="WebSiteDjango_DiogoRRoessler")

        if response is not None:
            print(F"Cookies Created with successful with name of: {response}")

        return response
