import pprint

from bson.objectid import ObjectId
from pymongo import MongoClient

import lib.lib_cosine.CommonNames as CN
import lib.lib_cosine.hierarchical_clustering as hierarchical
import lib.lib_cosine.temp_query_cosine as qur

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()


# ==============================




indexCollection = db[index_col_name]
documentCollection = db[document_col_name]

tf_docVector = db[tfvectDoc_col_name]


class browser():
    def __init__(self, parent=None):
        print("Debug: init browser")


    def query(self):

        # Empty the list
        # Get the words in the query

        text = input("search:")
        print("\nNews: \n")
        pprint.pprint(text)
        print("\n===============\n")


        words = qur.cleanQuery(text)
        # words = set(words)



        # print(words)
        # Collect the information for each word of the query
        index = {}
        for word in words:
            # print(word +" ")

            try:

                index[word] = indexCollection.find({'_id': word})[0]['info']
                # print(index[word])

            except :
                print("not found")


        # print('intex len =' ,tf_docVector.count())

        # Rank the documents according to the query
        results = qur.rankDocuments(index, words, db[document_col_name].count(),limit_of_rank=0.05)


        tt = []
        results.reverse()
        print("\n")
        for result in results:

            print("===========start===========")
            print("database id : "+str(result[0]) + ' similarity: ' + str((result[1]))+"\n")

            test = db[document_col_name].find_one({"_id": ObjectId(result[0])})
            print("News : "+test['data'])

            print("============end=============")


        doclist = [str(r[0]) for r in results]

        print("list == ",doclist,'\n  length = ',len(doclist))

        if len(doclist)!=0:
            # k_means.k_means(doclist)

            print("test",doclist[0])
            closest = doclist[0]
            clusters = hierarchical.hierarchical(doclist,0.1)

            index_of_serached_story = 0
            for c in clusters:
                flag = False
                for i in c:
                    if i == closest:
                        # print("Searched story group : ",doclist[0],"  ",closest)
                        list_r = list(clusters[index_of_serached_story])
                        list_r.reverse()

                        print(list_r)
                        # print(c)
                        flag =True
                        break

                if flag != False:
                    break

                index_of_serached_story +=1


            print("\n\nOther related story groups : ")

            ind = 0
            for c in clusters:
                if index_of_serached_story != ind:
                    print(c)

                ind += 1

            print ("\n\n\nSearched story group :")

            list_r = list(clusters[index_of_serached_story])
            list_r.reverse()

            for s in list_r:
                news_text = db[document_col_name].find({"_id":ObjectId(s)})

                print("==start==")
                print(news_text[0]['data'])
                print("==end==\n")


def search_main():
    myapp = browser()
    myapp.query()

def idf_search():
    pass


if __name__ == "__main__":

    # only tf ranking
    search_main()

    # idf ranking
    # cosine distance calculating
    # idf_search()
