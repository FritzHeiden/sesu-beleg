import urllib.request


class UrlHelper:

    @staticmethod
    def retrieve_url(url):
        response = urllib.request.urlopen(url)
        data = response.read()
        return data.decode("UTF-8")
