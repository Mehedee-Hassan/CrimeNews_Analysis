import math
import re
from math import log, sqrt

import snowballstemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymongo import MongoClient

import lib.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================



def cleanQuery(string):

    englishStopWords = stopwords.words('english')

    p = re.compile('\w+')
    words = p.findall(string)
    words = [word.lower() for word in words]
    engStem  =snowballstemmer.stemmer('english')

    words = [engStem.stemWord(word) for word in words]
    words = [word for word in words if word not in englishStopWords]
    return words


def nltkTockenizer(string):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(string)
    tokens = [token.lower() for token in tokens]

    engStem  =snowballstemmer.stemmer('english')
    englishStopWords = stopwords.words('english')

    tokens = [engStem.stemWord(token) for token in tokens]
    tokens = [token for token in tokens if token not in englishStopWords]


    return tokens


def rankDocuments(index1, words ,numberOfDocuments):
    # We rank each document based on query


    queryTfVector = queryDocTFcalc(words)

    # unique terms
    # words = list(set(words))
    print("***word = ",len(words))
    # document that has terms in query
    doclist = {}

    numofdoc = set()


    rankings = {}



    for word in words:

        try:

            index = db[index_col_name].find({'_id': word})[0]['info']
            # print(index[word])


        # if word in index:
            #
            # print(index[word])
            # continue

            for document_id in index['document(s)'].keys():

                numofdoc.add(document_id)

                # Term Frequency (log to reduce document size scale effect)
                TF = index['document(s)'][document_id]['frequency']
                DF = index['document frequency']
                doc_id = index['document(s)'][document_id]['doc_id']


                if TF > 0:
                    TF = 1 + log(TF,10)
                else:
                    TF = 0


                idf = numberOfDocuments / DF
                idf = log(idf ,10)

                tfidf = TF #* idf

                # todo : multiply idf

                if document_id not in doclist:
                    doclist[document_id] = []

                doclist[document_id].append((word ,tfidf))

        except:
            print(word ," not found")


    print("number of doc = ",len(numofdoc))

    ranklist = normalizedVector(doclist,queryTfVector)



    # Order results according to the scores
    # rankings = list(reversed(sorted(rankings.items(), key=lambda x: x[1])))

    ranklist = ((sorted(ranklist.items(), key=lambda x: x[1])))

    return ranklist

    

#  calculating normalization and cosine distance
def normalizedVector(doclist,queryTfVector):

    doc_ids = doclist.keys()

    print(len(doc_ids))


    ranking = {}

    sumofsq = 0
    for id in doc_ids:

        for element in doclist[id]:
            sumofsq += element[1]*element[1]

        sq = sqrt(sumofsq)

        temp_vector = {}

        for element in doclist[id]:
            temp_vector[element[0]] = element[1]/sq


        cosineValue = 0
        for key,value in temp_vector.items():

            cosineValue += temp_vector[key] * queryTfVector[key]


        cosineValue = round(cosineValue,4)

        if cosineValue > 0.09:

            ranking[id] = cosineValue
        else:
            # print("cosine =" ,cosineValue," ",id)
            test = 10
            # del ranking[id]

    return ranking



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
    for key ,value in temp_vect.items():

        if value > 0:
           value = 1+log(value,10)


        DF = getDFby(key)
        if DF == -1:
            DF = 1

        else:
            DF = numberOfDocs() / DF
            DF = math.log(DF,10)


        tfidf = value*DF


        sum += tfidf*tfidf


    sq = sqrt(sum)

    tmp = {}
    for key ,value in temp_vect.items():
        tmp[key] = temp_vect[key]/sq


    return tmp


def numberOfDocs():
    return db[document_col_name].count()

def getDFby(word):
    try:

        df = db[index_col_name].find({'_id':word})
        df = df['info']['document frequency']

        return  df

    except:
        return -1

