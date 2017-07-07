import math
import re
from math import sqrt

import snowballstemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymongo import MongoClient

import lib.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()


# ==============================



def cleanQuery(string):
    englishStopWords = stopwords.words('english')

    p = re.compile('\w+')
    words = p.findall(string)
    words = [word.lower() for word in words]
    engStem = snowballstemmer.stemmer('english')

    words = [engStem.stemWord(word) for word in words]
    words = [word for word in words if word not in englishStopWords]
    return words


def nltkTockenizer(string):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(string)
    tokens = [token.lower() for token in tokens]

    engStem = snowballstemmer.stemmer('english')
    englishStopWords = stopwords.words('english')

    tokens = [engStem.stemWord(token) for token in tokens]
    tokens = [token for token in tokens if token not in englishStopWords]

    return tokens


def computeVector(document_id):

    tfidfOfDocument = db[tfvectDoc_col_name].find_one({'_id':document_id})

    # print("type = ",type(tfidfOfDocument['_normtf']))

    return tfidfOfDocument['_normtf']




def cosineDistance(vectorA, vectorB):
    # print("vectorA = ", vectorA)
    # print("vectorB = " ,vectorB)

    tempSum = 0

    for key, val in vectorA.items():


        if key in vectorB:
            tempSum += (vectorA[key] * vectorB [key])

    return tempSum







def rankDocuments(index1, words, numberOfDocuments,limit_of_rank=0.1):
    # We rank each document based on query


    queryTfVector = queryDocTFcalc(words)


    tfidf_ofDocuments_list = db[tfvectDoc_col_name].find()


    ranking = {}
    for document in tfidf_ofDocuments_list:
        dbDocVector  =  computeVector(document['_id'])

        tempDistance = cosineDistance(dbDocVector , queryTfVector)

        if tempDistance > float(limit_of_rank):
            ranking[document['_id']] = tempDistance




    ranklist = ((sorted(ranking.items(), key=lambda x: x[1])))

    return ranklist










def queryDocTFcalc(words):
    temp_vect = {}
    for w in words:

        if w not in temp_vect:
            temp_vect[w] = 1

        else:
            temp_vect[w] += 1

    return queryDocNorm(temp_vect)


def queryDocNorm(temp_vect):
    sum = 0
    temp = {}
    for key, TF in temp_vect.items():

        if TF > 0:
            TF = 1 + math.log(TF, 10)
        else:
            TF = 0


        DF = getDFby(key)
        if DF == -1:
            DF = 1

        else:
            DF = numberOfDocs() / DF
            DF = math.log(DF, 10)

        tfidf = TF * DF

        temp[key] = tfidf

        sum += tfidf * tfidf

    sq = sqrt(sum)


    for key, TF in temp.items():
        temp[key] = temp[key] / sq



    return temp


def numberOfDocs():
    return db[document_col_name].count()


def getDFby(word):
    try:

        # print(word)

        df = db[index_col_name].find_one({'_id': word})['info']['document frequency']
        # df = df['info']['document frequency']

        # print(word ,'  ',df)

        return df

    except:

        # print("exception")
        print('')
        return -1

