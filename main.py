#!/usr/bin/env python3

"""
This is an image downloader script. It can take an input URL and download all the images from that web page.
"""

import sys

import url

if sys.version_info < (3, 0):
    raise SystemError("Please use python3\n")

import random
import time
import urllib.parse

from config import SUPPORTED_IMAGE_ATTRIBUTES, SUPPORTED_IMAGE_TYPES

try:
    import bs4 as bs
    import requests
except:
    raise ImportError("Please install beautifulsoup4 \n and requests modules for python3")

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/61.0.3163.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.56"]


class ImageDownloader:
    """scans a web page for all image links and downloads the images to a folder"""

    def __init__(self, url: str):
        self.url = url
        self.domain_name = urllib.parse.urlparse(self.url).hostname
        self.seq = 0

    def page_source(self):
        """ tries to connect to given URL via intermediate connector """
        print("Trying to connect to page...")
        try:
            req = self.intermediate_connector(self.url)
        except:
            try:
                print("error reconnecting...")
                req = self.intermediate_connector(self.url)
            except:
                raise ConnectionError("Check Your Internet Connection and URL")
        # print(req)
        return req

    @staticmethod
    def intermediate_connector(link: str):
        """waits for a random amount of time, uses user agents and connects to a webpage and downloads it """
        time.sleep(random.randrange(1, 5))
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(link, headers=headers)
        print("Connected")
        return response.content

    def find_images(self):
        """scans a beautiful soup object for all image links"""
        if self.get_file_type(self.url):
            self.save_image(self.url, "only")
            return None
        source = self.page_source()
        soup = bs.BeautifulSoup(source, 'html.parser')
        for image in soup.find_all("img"):
            tmp = image.get(SUPPORTED_IMAGE_ATTRIBUTES[0])
            name = image.get("alt")
            if tmp:
                self.call_save(tmp, name)
            else:
                try:
                    tmp = image.get(SUPPORTED_IMAGE_ATTRIBUTES[1])
                    self.call_save(tmp, name)
                except IndexError:
                    pass

    def call_save(self, tmp, name):
        if tmp:
            if tmp[:1] == "/":
                img_link = self.domain_name + tmp
            else:
                img_link = tmp
            self.seq += 1
            print("{} image found, checking image type...".format(str(self.seq)))
            self.save_image(img_link, name)

    @staticmethod
    def get_file_type(img_link: str):
        """returns the file type of image in passed image url"""
        if "data:image/jpeg;base64" in img_link:
            print("base64 image found:- no download support")
            return None
        for img_type in SUPPORTED_IMAGE_TYPES:
            if img_type in img_link:
                print(img_type)
                return img_type
        return None

    def save_image(self, img_link: str, name: str):
        """connects to the image link and saves the image with the correct extension """
        file_type = self.get_file_type(img_link)
        if file_type != None:
            if name is None:
                name = str(self.seq)
                print(name)
            time.sleep(random.randrange(1, 5))
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            try:
                img_req = requests.get(img_link, stream=True, headers=headers)
            except (requests.RequestException, requests.exceptions.InvalidURL) as e:
                print("{}, \nTRYING TO FIX\n".format(e))
                img_req = requests.get("http://" + img_link, stream=True, headers=headers)
            if img_req.status_code == 200:
                print("image downloaded, saving to file... {}".format(img_req.headers['Content-Type']))
                with open(name + file_type, 'wb') as img_file:
                    for chunk in img_req:
                        img_file.write(chunk)
                print("{} image saved".format(name))
        else:
            print(img_link)
            print("not a supported image")


if __name__ == "__main__":
    # a = "http://mapping.littlefreepantry.org/pantry/2704"

    link = "http://mapping.littlefreepantry.org/"
    urls = url.list_url(link)
    for links in urls:
        ImageDownloader(links).find_images()


    # ImageDownloader(a).find_images()