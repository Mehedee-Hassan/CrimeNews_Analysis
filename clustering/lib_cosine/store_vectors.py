
import sys, os
from pprint import pprint


import clustering.lib_cosine.parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient
import math

# Indexing
startTime = time.time()
index = {}



# database collection settings
import clustering.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================
def if_exists(collection,data):
    t= (collection.find({'_id':data}).count())
    print(t)
    if t>0:
        return True
    else:
        return False

def TFVectorForDoc():

    cursor = db[index_col_name].find()
    db[tfvectDoc_col_name].count()
    total_doc = db[document_col_name].count()

    print("total== ",total_doc)
    print(cursor)
    docs = {}
    print("here")


    for word_index in cursor:
        d = word_index['info']['document(s)']
        d2 = list(word_index['info']['document(s)'].keys())

        print('_')
        for doc_id_as_key in d2:
            print('+')

            #  if document exists in tf_doc_vector



            if db[tfvectDoc_col_name].find({'_id':doc_id_as_key}).count()  <= 0:

                # insert in to tfdocvector

                tempTf = d[doc_id_as_key]['frequency']

                if tempTf > 0:
                    tempTf = 1 + math.log(tempTf, 10)
                else:
                    tempTf = 0

                tempDF = word_index['info']['document frequency']
                tempIDF = total_doc / tempDF
                tempIDF = math.log(tempIDF, 10)

                tfidf =  ( tempTf*tempIDF )

                print ("tf",tempTf ,"id - ",tempDF," idf =",tempIDF)
                db[tfvectDoc_col_name].insert_one({
                    '_id': doc_id_as_key,
                    '_tf': {word_index['_id']:tfidf}
                })


            #  if document doesnt exist in the tf_doc_vector
            else:
                try:
                    # get the list of tf

                    tf_list = ((db[tfvectDoc_col_name].find_one({'_id': doc_id_as_key})))

                    tf_list = (tf_list['_tf'])

                    tempTf = d[doc_id_as_key]['frequency']

                    if tempTf > 0 :
                        tempTf = 1 + math.log(tempTf, 10)
                    else:
                        tempTf = 0


                    tempDF = word_index['info']['document frequency']
                    tempIDF = total_doc / tempDF
                    tempIDF = math.log(tempIDF, 10)

                    tfidf = (tempTf * tempIDF)

                    # append new object to old one


                    tf_list[word_index['_id']] = tfidf
                    # pprint(tf_list)



                    # pprint(tf_list)

                    # update collection
                    print("tf", tempTf, "id - ", tempDF, " idf =", tempIDF)

                    db[tfvectDoc_col_name].update_one(
                        {'_id': doc_id_as_key},
                        {
                            "$set": {
                                '_tf': tf_list
                            }
                        }
                    )

                except:
                    print("null")

              # docs[doc_id_as_key][document['_id']] = d[doc_id_as_key]['frequency']
    print("here")



def saveNormalization():
    data = db[tfvectDoc_col_name].find()

    for element in data:

        pprint(element)
        sumtf = 0
        for tf in element['_tf'].items():

            # pprint(tf)
            # pprint(tf[1])

            sumtf += (tf[1]*tf[1])


        print(sumtf)
        sq = math.sqrt(sumtf)



        normlist = {}

        for tf in element['_tf'].items():

            tempNorm = tf[1]/sq
            normlist[tf[0]] = (tempNorm)

        try:


            # update collection

            db[tfvectDoc_col_name].update_one(
                {'_id': element['_id']},
                {
                    "$set": {"_normtf":normlist}
                }


            )

        except:
            print("null")


 # save normalized vector for each document's words


TFVectorForDoc()

# save normalized vector for each document's words
saveNormalization()