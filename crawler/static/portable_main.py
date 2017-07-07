from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import newspaper
import crawler.static.writeFileToDisk

import time


__filename_global = 0


def readFromFile():

    allLinks = []
    with open("dailystar/tonu_rape","r") as f:
        for line in f:
            allLinks.append(line)


    return allLinks




def html_dl(url):

    linkNow = url


    if "http" in linkNow or "www" in linkNow:

        try:
            response = urlopen(linkNow)

            print("==getlinks", str(response.getheader('Content-Type')))

            if 'text/html' in str(response.getheader('Content-Type')):

               htmlBytes = response.read()
               htmlString = htmlBytes.decode("utf-8")



               global __filename_global
               __filename_global = __filename_global + 1



        except :
            print("failed to open ********")

