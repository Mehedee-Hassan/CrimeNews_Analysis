import html
import pprint
import re
from html.parser import HTMLParser
from threading import Thread

import newspaper
import nltk
import numpy
import sklearn.svm
import os

import sys

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer,ENGLISH_STOP_WORDS
from sklearn.externals import joblib
import pickle
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
import nltk.data

import os
import sys

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

import location.sentence_with_loc.ne_filter  as SWL

import location

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

import location.sentence_with_loc.ne_filter  as SWL
from pprint import  pprint
from pymongo import MongoClient
import nltk
import location.sentence_with_loc.gazetteer as gaztteer
# database collection settings
import lib.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()


# ==============================
indexCollection = db[index_col_name]
documentCollection = db[document_col_name]

tf_docVector = db[tfvectDoc_col_name]





def read_data(path):
    files = os.listdir(path)

    p1 = path+"/"
    data = []


    for file in files:


        reader = open(p1+file ,"r")

        text = reader.read()

        data.append(text)

        reader.close()

    return data


def read_from_disk_training():



    data_with_label = []

    print(root_path_current_dir)

    for root, subdirs, files in os.walk(root_path_current_dir):
        print("root = ", root)
        current_subdir  = root.split(os.sep)[-1]

        for file in files:



            # if 'crime' not in current_subdir.title().lower() or 'ncrime' not in current_subdir.title().lower() :
            #     print("**", current_subdir.title().lower())
            #     continue


            path = root_path_current_dir +current_subdir+"\\"+ file



            reader = open(str(path), "r",encoding="latin-1")
            text = reader.readlines()[1:]
            text = ''.join(text)

            # read crime training data
            if current_subdir == "crime":

                # print("s = ", root.split(os.sep)[-1], "f = ", file)
                data_with_label.append((text,"crime"))
                reader.close()
            # read not crime data
            elif current_subdir == "ncrime":
                # print("s = ", root.split(os.sep)[-1], "f = ", file)
                data_with_label.append((text,"ncrime"))
                reader.close()



    return data_with_label


def read_for_sentence_training():

    data_with_label = []

    print(root_path_current_dir)


    file_neg = root_path_current_dir+'\\data\\crime_loc_sent_neg'
    file1_pos = root_path_current_dir+'\\data\\crime_loc_sent_pos'


    file_reader = open(file1_pos , 'r')

    poslines = file_reader.readlines()
    poslines = [p for p in poslines if p != '']

    for lines in poslines:
        data_with_label.append((lines,'CL'))

    file_reader.close()

    file_reader = open(file_neg , 'r')

    neglines = file_reader.readlines()
    neglines = [p for p in neglines if p != '']

    for lines in neglines:
        data_with_label.append((lines,'NCL'))

    file_reader.close()





    return data_with_label


def get_custom_stop_words():

    return ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once'
        , 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do'
        , 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am'
        , 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are'
        , 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself'
        , 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had'
        , 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in'
        , 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can'
        , 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only'
        , 'myself', 'which', 'those', 'i', 'after'
        , 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a'
        , 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than','the','of'

        # location names
        ,'Bangladesh','dhaka','bangladesh','barisal',
            'barguna',            'barisal',            'bhola',            'jhalokati',
            'patuakhali',            'pirojpur',            'chittagong',            'bandarban',
            'brahmanbaria',            'chandpur',            'chittagong',            'comilla',
            'cox\'s bazar',            'feni',            'khagrachhari',            'lakshmipur',
            'noakhali',            'rangamati',            'dhaka',            'faridpur',
            'gazipur',            'gopalganj',            'jamalpur',            'kishoregonj',
            'madaripur',            'manikganj',            'munshiganj',            'mymensingh',
            'narayanganj',            'narsingdi',            'netrakona',            'rajbari',
            'shariatpur',            'sherpur',            'tangail',   'shibganj','abdullahpur'
        # people / organization
            'prothom','begum','begumganj','abdul', 'abdul-jabbar',  'abdulahi','abdullah',
            'abdullah-al-baki',  'abdullah-al-harun',  'abdullah-hel-baki','abdurashid',
            'abul','shahi',  'shahid',  'shahida' , 'shahidul' , 'shahidulla' , 'shahidullah'  ,'shahidur'
        # day names
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",  "sunday"
        # moth names
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november','december'
        ]




def train(data_to_train):


    my_words = get_custom_stop_words()


    my_stop_words = ENGLISH_STOP_WORDS.union(my_words)


    vectorizer = TfidfVectorizer(min_df=1,
                                 max_df = 0.8,
                                 sublinear_tf=True,
                                 use_idf =True,
                                 lowercase=True,
                                 stop_words=my_stop_words,
                                 # tokenizer=LemmaTokenizerFuction
                                 )


    toLammatize_array= [text[0] for text in data_to_train]
    #
    # # wordnet_lemmatizer = WordNetLemmatizer()
    # snowball_stemmer = SnowballStemmer("english")
    #
    #
    # x_data_to_re_number = [snowball_stemmer.stem(item) for item in toLammatize_array]

    x_data = [re.sub('[0-9]+' ,'',item) for item in toLammatize_array]


    # print(x_data[0])

    # print (data_to_train[0])

    print ("here ---")

    train_x = vectorizer.fit_transform(x_data)

    print(train_x[0].todense())

    train_x_label = [label[1] for label in data_to_train]

    svmModel = sklearn.svm.SVC(kernel="linear")

    svmModel.fit(train_x,train_x_label)




    return svmModel,vectorizer



i = 0


def StemTokenizerFuction(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(nltk.PorterStemmer().stem(item))

    global i
    i+=1
    if i < 10:
        print (stems[0:20])

    return stems

def LemmaTokenizerFuction(text):
    tokens = nltk.word_tokenize(text)
    lemma = []
    punctuation = string.punctuation


    for item in tokens:

        item = item.strip(punctuation)
        item = nltk.WordNetLemmatizer().lemmatize(item,pos='v')
        lemma.append(nltk.WordNetLemmatizer().lemmatize(item))



    global i
    i+=1
    if i < 10:
        print (lemma[0:20])

    return lemma


def validateClassifier(X,y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.50 ,train_size=0.50)

    svmModel = sklearn.svm.SVC(
        # kernel="linear"
        gamma=0.001,
        C=1000
    )

    svmModel.fit(X_train, y_train)

    y_true ,y_pred = y_test,svmModel.predict(X_test)

    print(classification_report(y_true, y_pred))
    print()
    print('--confusion matrix--')
    print(confusion_matrix(y_true, y_pred))
    print()





def read_test_file(model,vectorizer):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


    files = os.listdir(root_path_current_dir+"\\test_data\\")
    # print("debug## read test ",root_path_current_dir)

    test = []
    for file in files:
        p1 = root_path_current_dir+"\\test_data\\"+file
        if os.path.isfile(p1):

            reader = open(p1,"r",encoding="utf8")

            text = reader.read()
            # test.append(text)
            reader.close()

            sents = SWL.line_token(text)
            # print("debug## predict")

            for s in sents:


                print("\n==== ====\ntest file = ",file )

                print("News Title = ",s)


                print("result=")

                predict([s[0]], model, vectorizer,file)



    # return test

    # for t in test:
    #     predict([t],model,vectorizer)


non_crime_data=[]
crime_data=[]

def predict(data,model,vectorizerTfIdf,file = ""):



    test_x = vectorizerTfIdf.transform(data)

    feature_name = vectorizerTfIdf.get_feature_names()

    # print("debug## predict")



    result = model.predict(test_x)

    # print("debug##",result)

    # display the data with feature name
    # ======================================
    feature_vector = numpy.round(test_x.todense(), 2)
    # display_features(feature_name, feature_vector)
    # ======================================



    return test_x,result



def download_test():

    _current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # links to check

    links = [
        # "http://www.thedailystar.net/country/death-buffalos-caused-rotten-grass-sunamganj-haor-1397368",
        # "http://www.thedailystar.net/country/2-held-nganj-over-torturing-expats-libya-1397428",
        # "http://www.thedailystar.net/frontpage/uranium-behind-deaths-haors-1394068",
        # "http://en.prothom-alo.com/bangladesh/news/146549/4-killed-in-operation-Eagle-Hunt",
        # "http://en.prothom-alo.com/bangladesh/news/146577/Over-100-000ha-of-Boro-cropland-flooded-in"
        # "http://www.thedailystar.net/news-detail-268652",
        "http://www.thedailystar.net/news/restricted-she-killed-parents",
        # "http://www.thedailystar.net/frontpage/3-family-burned-dead-1367344",
        # "http://archive.thedailystar.net/forum/2012/July/road.htm",
        # "http://www.thedailystar.net/backpage/7-hurt-factory-guards-open-fire-protesters-1201078",
        # "http://www.thedailystar.net/frontpage/48-feared-dead-pia-plane-crash-1326838",
        # "http://en.prothom-alo.com/bangladesh/news/146723/Meat-traders-likely-to-go-on-strike-in-Ramadan",
        # "http://en.prothom-alo.com/bangladesh/news/146721/Slums-harbouring-criminals-to-be-evicted-IGP"

    ]
    __path = root_path_current_dir+"\\test_data\\"

    file_name_incr = 0

    for link in links:





        a = newspaper.Article(link)
        a.download()
        a.parse()


        txt_title = __path + str(file_name_incr) + ".txt"


        print(txt_title)
        reader = open(txt_title, "w+", encoding='UTF8')
        reader.write(a.title+"."+"\n"+a.text)

        reader.close()
        file_name_incr+=1




def save_model_to_disk(model_to_save,vectorizer):
    path_model = "model/"
    file_model = "svc-sentence.pkl"
    file_vect = "tfidf-vectorizer-sentence.pkl"
    file_custom_tokenizer = "stem-tokenizer-for-tfidfvect.pkl"


    joblib.dump(model_to_save,path_model+file_model)
    joblib.dump(vectorizer ,path_model+file_vect )



def display_features(features_names,features):
    df = pd.DataFrame(data=features,columns=features_names)
    pd.set_option('display.max_columns', None)

    print (df)




def Main():


    __path = "/data/crime"

    numpy.set_printoptions(threshold=numpy.nan)
    data_as_array = read_for_sentence_training()



    model ,vectorizer =train(data_as_array)

    print('find1')
    save_model_to_disk(model,vectorizer)

    downalod_thread = Thread(target=download_test,args=())

    # download_test()

    print("debug## main")

    file_read_thread = Thread(target=read_test_file,args=(model,vectorizer))

    downalod_thread.start()
    downalod_thread.join()



    file_read_thread.start()
    file_read_thread.join()

    # data_to_Test = read_test_file()
    print(non_crime_data)



def readFromDB(docnum=0):

    for data in db[document_col_name].find().limit(100):

        docnum += 1
        text = data ['data']

        sents = tokenizer.tokenize(text)

        for s in sents:
            str2 = str(docnum) + '|' + s +'\n\n'
            # reader1.write(str2)

            temp ,list = preTrainedNLTK(s)

            sum1 += temp

            print("sum = ",sum1)

            if len(list)!=0:
                print(docnum)
                # reader2.write("nltk "+str(docnum)+"|"+s+"\n\n")



def loadModel():

    model_path = root_path_current_dir + '\\model\\svc-sentence.pkl'
    vectorizer_path = root_path_current_dir + '\\model\\tfidf-vectorizer-sentence.pkl'


    model = joblib.load(model_path)
    vect = joblib.load(vectorizer_path)

    return model,vect



def readSingle(text):

     model ,vect = loadModel()
     sents = SWL.line_token(text)

     # print("debug## crime sentence ",sents)
     locations = []

     for s in sents:

         text_x, result = predict([s[0]], model, vect)

         # name = s[1][0][0][0]
         names = []

         for n in s[1]:
            # print("debug## ",n)
            full_name = ""
            for n_part in n:
                if full_name == "":
                    full_name = full_name + n_part[0]
                else:
                    full_name += " "+ n_part[0]

            names.append(full_name)


         # print (result)
         # print(names)

         if result == 'CL':
             locations.extend(names)

     # print("crime location related to this news = ",locations)

     return set(locations)


if __name__ == "__main__":
    root_path_current_dir = os.path.dirname(location.sentence_with_loc.__file__)

    Main()


else:
    root_path_current_dir = os.path.dirname(location.__file__)



