import time

import newspaper
from pymongo import MongoClient

from crawler.util import Counter
from db import CommonNames as CN

client = MongoClient()
db = CN.RawDb.getDatabase(client)

onlineNewsColName = CN.RawDb.getOnlineCollection()
indexNewsColName = CN.RawDb.getNewsIndexCollection()

def saveHtmlToDb(link,response):

        try:

            print (link)
            # print("html = ",response)

            if '/bangla/' in link:
                return False

            print("debug## article parse start")

            newsArticle = newspaper.Article(url="")
            newsArticle.set_html(response)

            newsArticle.parse()

            print("debug## article parse end")

            title = (newsArticle.title) + "."


            # if bangla title dont save

            for achar in title:
                if achar <= '\u09FA' and achar >= '\u0981':
                    return False



            text = title + "\n" + (newsArticle.text)



            print("debug##",title)

            storeDocument(link,title,text,onlineNewsColName)

            Counter.Counter.cnt += 1

        except:
            print("failed to save ********")

        print("\n\nDocument saved ",Counter.Counter.cnt)
        print("Run time : ", round(time.time() - Counter.Counter.runTime , 2) ," seconds")
        print("\n\n")

def storeDocument(link ,title,text , col_name):

    if ifExsits(link) == False:
        return False

    print("debug## document store")

    collection = db[col_name]
    documentId = collection.save({'title': title, 'text' :text})

    saveToIndex(link,title,documentId)

    return True


def ifExsits(link):

    if db[indexNewsColName].find({'_Id':link}).count() > 0:
        print("debug## document store count")

        return False

    return True

def saveToIndex(link,title,documentId):


    print("debug## index store")

    collection = db[indexNewsColName]
    collection.save({'_id': link,'title': title ,'documentId':str(documentId)})


    return True