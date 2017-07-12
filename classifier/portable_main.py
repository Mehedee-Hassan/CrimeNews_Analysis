from threading import Thread

import nltk
from sklearn.externals import joblib
import numpy
import os
import classifier
from classifier.db_handle.db_retrieve import Retrieve

this_file_path = os.path.dirname(classifier.__file__)


import db.CommonNames as CN

from pymongo import MongoClient

client = MongoClient()
_testDb = CN.TestDb.getDatabase(client)
_rawDb = CN.RawDb.getDatabase(client)


crime_news_list = []
n_crime_news_list = []


def saveToDocumentDb(path,data,name):

    file = open(path+"\\"+name+".txt" , 'w')
    file.write((str(data.encode('UTF-8'))))
    file.close()



def classifyWithSavedModel(model,vectorizer):
    #
    # retrieve = Retrieve()
    # idlist = retrieve.getTotalData()
    #
    #
    # for id in idlist:
    #
    #     if retrieve.notInDocument(id['_id']) == True:
    #         text = retrieve.getData(id['_id'])

    database = _rawDb[CN.RawDb.getOnlineCollection()]

    incr = 0
    for element in database.find({}):
        print(element['text'])

        text = element['title']+"."+element['text']

        res = predict([text],model,vectorizer,element['title'])

        if res == 'crime':
            saveToDocumentDb(temp_crime_files,text,str(incr))
        else:
            saveToDocumentDb(temp_n_crime_files,text,str(incr))

        incr += 1




def predict(data, model, vectorizerTfIdf, file):
    test_x = vectorizerTfIdf.transform(data)

    feature_vector = numpy.round(test_x.todense(), 3)


    result = model.predict(test_x)

    if result[0] == 'ncrime':
        n_crime_news_list.append(str(file))

    if result[0] == 'crime':
        crime_news_list.append(str(file))


    print(result)

    return result[0]

def StemTokenizerFuction(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(nltk.PorterStemmer().stem(item))
    return stems

def LemmaTokenizerFuction(text):

    import string
    tokens = nltk.word_tokenize(text)
    lemma = []
    punctuation = string.punctuation


    for item in tokens:

        item = item.strip(punctuation)
        item = nltk.WordNetLemmatizer().lemmatize(item,pos='v')
        lemma.append(nltk.WordNetLemmatizer().lemmatize(item))


    return lemma



def loadModels():

    model_path = this_file_path + '\\model\\svc-linear-cr1460ncr1035.pkl'
    vectorizer_path = this_file_path + '\\model\\tfidf-vectorizer-cr1460ncr1035.pkl'


    model = joblib.load(model_path)
    vect = joblib.load(vectorizer_path)

    return model,vect


def classify_and_save():

    __path = "/data/crime"

    # show all data in numpy array
    numpy.set_printoptions(threshold=numpy.nan)


    # load pretrained saved model



    model,vectorizer = loadModels()

    print("loaded ..")


    # download_test()

    file_read_thread = Thread(target=classifyWithSavedModel, args=(model, vectorizer))



    file_read_thread.start()
    file_read_thread.join()

    # data_to_Test = read_test_file()
    print(n_crime_news_list)



def documentClassify(document,model,vect):
    test_x = vect.transform([document])

    result = model.predict(test_x)

    return result[0]


def singleDocClassify(document):

    flag = 'crime'
    model ,vect = loadModels()
    flag = documentClassify(document,model, vect)

    return flag


if __name__=='__main__':

    root_path = os.path.abspath('..')
    print(root_path)
    temp_crime_files = root_path + "\\temp_files\\crime"
    temp_n_crime_files = root_path + "\\temp_files\\ncrime"

    classify_and_save()

    print ("non crime: ", len(n_crime_news_list))
    print ("crime: ", len(crime_news_list))

else:
    root_path = os.path.abspath('.')
    print(root_path)
    temp_crime_files = root_path + "\\temp_files\\crime"
    temp_n_crime_files = root_path + "\\temp_files\\ncrime"
