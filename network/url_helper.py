import requests
import math
import datetime
import os

class UrlHelper:
    @staticmethod
    def __bytes_to_megabytes(bytes):
        return math.floor(bytes/10000)/100

    @staticmethod
    def __get_current_timestamp():
        return '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
    # download and decode content from a specific url
    @staticmethod
    def retrieve_url(url):
        response = requests.head(url)
        content_length = int(response.headers["content-length"])
        print("Fetching {1}MB of data from '{0}'".format(url, UrlHelper.__bytes_to_megabytes(content_length)))
        byte_step_size = 1000000
        document = b''
        file_path = "./article-download-tmp"
        file = open(file_path, "wb")
        for i in range(0, content_length, byte_step_size):
            start = i
            end = i + byte_step_size - 1

            if end > content_length:
                end = content_length
            headers = {"Range": "bytes={0}-{1}".format(start, end)}
            response = requests.get(url, headers=headers)
            file.write(response.content)
            print("Download progress: {0}% ({1}/{2}MB)".format(
                math.floor(end / content_length * 10000)/100,
                UrlHelper.__bytes_to_megabytes(end),
                UrlHelper.__bytes_to_megabytes(content_length)
            ))

        file.close()
        file = open(file_path, "r")
        document = file.read()
        file.close()
        os.remove(file_path)
        return document

        # request = Request(url)
        # request.add_header
        # response = urllib.request.urlopen(url)
        # data = response.read()
        # return data.decode("UTF-8")
