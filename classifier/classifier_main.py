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
from sklearn.feature_extraction.text import TfidfVectorizer,ENGLISH_STOP_WORDS
from sklearn.externals import joblib
import pickle
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

import classifier.db_handle as databaseh



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

    root_path_current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    root_path_current_dir += "\\data\\"

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
            'shariatpur',            'sherpur',            'tangail',   'shibganj','abdullahpur','kolkata',
            'sudan','india','saudi','libya','ghora','aha','thailand','thai','burma','sri','israel','london',
            'pakistan','afganistan','iraq','iran',
        # people / organization
            'prothom','begum','begumganj','abdul', 'abdul-jabbar',  'abdulahi','abdullah',
            'abdullah-al-baki',  'abdullah-al-harun',  'abdullah-hel-baki','abdurashid',
            'abul','shahi',  'shahid',  'shahida' , 'shahidul' , 'shahidulla' , 'shahidullah'  ,'shahidur',
            'farah','ruma','rafiq','rafi','mannam','asad','asaduzzaman','abul','kasem','manik','rabbi',
            'barek','kalam','minar','gulam','azam',
        # day names
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",  "sunday",
        # moth names
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november','december',
            'robi','italy','premier','league','europa','gazi',
        ]




def train(data_to_train,flag='n'):


    my_words = get_custom_stop_words()


    my_stop_words = ENGLISH_STOP_WORDS.union(my_words)


    vectorizer = TfidfVectorizer(min_df=10,
                                 max_df = 0.5,
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

    # print(train_x[0].todense())


    print (numpy.shape(train_x))
    train_x_label = [label[1] for label in data_to_train]

    print(len(train_x_label))

    svmModel = sklearn.svm.SVC(
        # kernel="linear"
        gamma=0.001,
        C=1000
    )

    svmModel.fit(train_x,train_x_label)

    # uncomment to validate
    # =====================
    # grid search to tune parameter
    # warning : no label found for few data
    # GridSearchParameterTune(train_x,train_x_label)
    # validate classifier
    if flag == 'y' or flag == 'yes':
        validateClassifier(train_x,train_x_label)
    # ======================

    return svmModel,vectorizer



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


def GridSearchParameterTune(X,y):


    X_train, X_test, y_train, y_test = train_test_split(
        X, y,  random_state=5 ,test_size=.6)



    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100, 1000 ]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    scores = ['precision', 'recall' ]

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
                           scoring='%s_macro' % score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)

        print(classification_report(y_true, y_pred))
        print()
        print('--confusion matrix--')
        print(confusion_matrix(y_true,y_pred))
        print()


# ==== end of grid search ===== #




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




def read_test_file(model,vectorizer):

    root_path_current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    root_path_current_dir += "\\test_data\\test_data\\"

    files = os.listdir(root_path_current_dir)

    test = []
    for file in files:
        p1 = root_path_current_dir+file
        if os.path.isfile(p1):

            reader = open(p1,"r",encoding="utf8")

            text = reader.read()
            # test.append(text)
            reader.close()

            reader = open(p1,"r",encoding="utf8")
            news_title = reader.readline()
            reader.close()

            print("\n==== ====\ntest file = ",file )
            if news_title != None:
                print("News Title = ",news_title)


            print("result=")

            predict([text], model, vectorizer,file)



    # return test

    # for t in test:
    #     predict([t],model,vectorizer)


non_crime_data=[]

def predict(data,model,vectorizerTfIdf,file):



    test_x = vectorizerTfIdf.transform(data)

    feature_name = vectorizerTfIdf.get_feature_names()

    # display the data with feature name
    # ======================================
    # feature_vector = numpy.round(test_x.todense(), 2)
    # display_features(feature_name, feature_vector)
    # ======================================



    result = model.predict(test_x)

    if result[0] == 'ncrime':
        non_crime_data.append(str(file))

        print ("not crime news")
    else :
        print ("crime related news")

    return test_x



def download_test():

    _current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # links to check

    links = [
        # "http://www.thedailystar.net/country/death-buffalos-caused-rotten-grass-sunamganj-haor-1397368",
        # "http://www.thedailystar.net/country/2-held-nganj-over-torturing-expats-libya-1397428",
        # "http://www.thedailystar.net/frontpage/uranium-behind-deaths-haors-1394068",
        # "http://en.prothom-alo.com/bangladesh/news/146549/4-killed-in-operation-Eagle-Hunt",
        # "http://en.prothom-alo.com/bangladesh/news/146577/Over-100-000ha-of-Boro-cropland-flooded-in"
        # "http://www.thedailystar.net/country/bangladeshi-girl-dies-california-plane-crash-1361062",
        # "http://www.thedailystar.net/news/restricted-she-killed-parents",
        # "http://www.thedailystar.net/frontpage/3-family-burned-dead-1367344",
        # "http://archive.thedailystar.net/forum/2012/July/road.htm",
        # "http://www.thedailystar.net/backpage/7-hurt-factory-guards-open-fire-protesters-1201078",
        # "http://www.thedailystar.net/frontpage/48-feared-dead-pia-plane-crash-1326838",
        # "http://en.prothom-alo.com/bangladesh/news/146723/Meat-traders-likely-to-go-on-strike-in-Ramadan",
        # "http://en.prothom-alo.com/bangladesh/news/146721/Slums-harbouring-criminals-to-be-evicted-IGP",
        "http://www.newagebd.net/article/19222/4-jmb-men-arrested",
        "http://www.newagebd.net/article/19229/80kg-venison-two-deer-heads-skin-seized-in-bagerhat",
        "http://www.newagebd.net/article/19234/five-du-students-among-26-held-for-taking-drugs",
        "http://www.newagebd.net/article/19226/two-killed-in-magura-road-accident",
        "http://www.newagebd.net/article/19239/ju-upgrades-job-offer-to-ac-robiuls-wife-after-criticism",
        "http://www.newagebd.net/article/19157/implement-budget-dev-projects-speedily-pm-asks-officials"

    ]
    __path = _current_dir+"\\test_data\\test_data\\"

    file_name_incr = 0

    for link in links:





        a = newspaper.Article(link)
        a.download()
        a.parse()


        txt_title = __path + str(file_name_incr) + ".txt"


        print(txt_title)
        reader = open(txt_title, "w+", encoding='UTF8')
        reader.write(a.title+"\n"+a.text)

        reader.close()
        file_name_incr+=1


def save_model_to_disk(model_to_save,vectorizer):
    path_model = "model/"
    file_model = "svc-linear-cr1460ncr1035.pkl"
    file_vect = "tfidf-vectorizer-cr1460ncr1035.pkl"
    file_custom_tokenizer = "stem-tokenizer-for-tfidfvect.pkl"


    joblib.dump(model_to_save,path_model+file_model)
    joblib.dump(vectorizer ,path_model+file_vect )



def display_features(features_names,features):
    df = pd.DataFrame(data=features,columns=features_names)
    pd.set_option('display.max_columns', None)

    print (df)




def Main():


    aa = input("Download and test (y/n):")

    __path = "/data/crime"

    numpy.set_printoptions(threshold=numpy.nan)
    data_as_array = read_from_disk_training()


    # ======================
    # uncomment to validate in train block
    # =====================



    model ,vectorizer =train(data_as_array,aa)


    if aa == 'n' or aa == 'N' or aa == 'no':
        return

    print('debug### : find1')


    save_model_to_disk(model,vectorizer)



    # ==================online download==========================
    # online data download and classification
    downalod_thread = Thread(target=download_test,args=())
    # # download_test()
    file_read_thread = Thread(target=read_test_file,args=(model,vectorizer))
    #
    downalod_thread.start()
    downalod_thread.join()
    file_read_thread.start()
    file_read_thread.join()
    #
    # ==================online download==========================


    # ==================data base test==========================



    # ==================data base test==========================





    # data_to_Test = read_test_file()
    print(non_crime_data)





if __name__ == "__main__":



    Main()





