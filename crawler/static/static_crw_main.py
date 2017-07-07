from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import newspaper
import crawler.static.writeFileToDisk

import time


__filename_global = 0



# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def readFromFile():

    allLinks = []


    # with open("links_not_crime_accident","r") as f:
    #     for line in f:
    #         allLinks.append(line)


    # with open("dailystar/all_links_crime_dailystar.txt","r") as f:
    # with open("dailystar/7-murder","r") as f:
    with open("dailystar/tonu_rape","r") as f:
        for line in f:
            allLinks.append(line)


    return allLinks




def spider(url):


    numberVisited = 0
    pagesToVisit = []
    visitedPage = []

    pagesToVisit = readFromFile()

    print (len(pagesToVisit))


    size = len(pagesToVisit)



    while numberVisited < size and pagesToVisit != []:


        linkNow = pagesToVisit.pop()

        if "http" in linkNow or "www" in linkNow:
    #         yes this is a link

            # visitedPage.append(linkNow)

            try:
                response = urlopen(linkNow)

                print("==getlinks", str(response.getheader('Content-Type')))

                if 'text/html' in str(response.getheader('Content-Type')):

                    htmlBytes = response.read()
                    htmlString = htmlBytes.decode("utf-8")



                    global __filename_global
                    __filename_global = __filename_global + 1
                    numberVisited += 1

                    webscrapping.static_crawler.writeFileToDisk.writeFile(contentHtml=htmlString,__filename=str(__filename_global),url=url)

            except :
                print("failed********")

            time.sleep(0.6)


list_of_lisnk = [

]


spider("jhg")
