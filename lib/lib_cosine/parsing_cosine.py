import re

import snowballstemmer
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from pymongo import MongoClient

import lib.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================




englishStopWords = stopwords.words('english')
p = re.compile('\w+')

def clean(data):
    # Concatenate the lines into a big string
    # words = [word for word in ' '.join(data).split(' ')]
    # Search every word in the big string
    # words = p.findall(' '.join(words))
    # Lower case

    tokenizer = RegexpTokenizer(r'\w+')

    words = tokenizer.tokenize(data)

    words = [word.lower() for word in words]
    # Stem word
    englishStem = snowballstemmer.stemmer('english')
    words = [englishStem.stemWord(word) for word in words]
    # Remove stop words
    words = [word for word in words if word not in englishStopWords]
    # Done!
    return words


def clean_lines(data):
    # Concatenate the lines into a big string
    # words = [word for word in ' '.join(data).split(' ')]
    # Search every word in the big string
    # words = p.findall(' '.join(words))
    # Lower case
    tokenizer = RegexpTokenizer(r'\w+')
    # Stem word
    englishStem = snowballstemmer.stemmer('english')
    line_word = []

    for d in data:

        words = tokenizer.tokenize(d)
        words = [word.lower() for word in words]
        words = [englishStem.stemWord(word) for word in words]
        # Remove stop words
        words = [word for word in words if word not in englishStopWords]
        line_word.extend(words)



    # Done!
    return line_word


def index( words, index, id):

    doc_id = str(id)

    for word in words:

        # If the word is not in the index
        if word not in index:

            index[word] = {
                           'document frequency' : 1,
                           'document(s)' : {
                                            doc_id : {
                                                         'frequency' : 1,
                                                         'doc_id'    : id
                                                     }
                                            }
                           }
        # If the word is in the index
        else:
            # index[word]['term frequency'] += 1

            # If the word has not been found in this document
            if doc_id not in index[word]['document(s)'].items():

                index[word]['document frequency'] += 1

                index[word]['document(s)'][doc_id] =  {
                                                        'frequency' : 1,
                                                        'doc_id': id
                                                      }


            # If the word has been found in this document
            else:
                 index[word]['document(s)'][doc_id]['frequency'] += 1


    return index




def make_term_index( words, index, id):

    doc_id = str(id)

    # print(words)

    for word in words:

        # If the word is not in the index

        index_word = db[index_col_name].find_one({'_id':word})

        # pprint(db[index_col_name].find({'_id':word}).count())

        if db[index_col_name].find({'_id':word}).count() <= 0:

            db[index_col_name].insert_one(
                                {
                                        '_id': word,
                                        'info':
                                        {
                                        'document frequency' : 1,
                                        'document(s)' : {
                                                        doc_id : {
                                                                     'frequency' : 1,
                                                                     'doc_id'    : doc_id
                                                                 }
                                        }               }
                                }
            )


        # If the word is in the index
        else:
            # index[word]['term frequency'] += 1

            # If the word has not been found in this document


            # print(index_word)
            temp = (index_word['info']['document(s)'])


            if doc_id not in temp.keys():

                index_word['info']['document frequency'] += 1

                index_word['info']['document(s)'][doc_id] =  {
                                                        'frequency' : 1,
                                                        'doc_id': doc_id
                                                      }


            # If the word has been found in this document
            else:
                index_word['info']['document(s)'][doc_id]['frequency'] += 1




            db[index_col_name].save(index_word)


    # return index


def make_term_index_by_db( words, index, id,db,index_col_name):

    doc_id = str(id)

    # print(words)

    for word in words:

        # If the word is not in the index

        index_word = db[index_col_name].find_one({'_id':word})

        # pprint(db[index_col_name].find({'_id':word}).count())

        if db[index_col_name].find({'_id':word}).count() <= 0:

            db[index_col_name].insert_one(
                                {
                                        '_id': word,
                                        'info':
                                        {
                                        'document frequency' : 1,
                                        'document(s)' : {
                                                        doc_id : {
                                                                     'frequency' : 1,
                                                                     'doc_id'    : doc_id
                                                                 }
                                        }               }
                                }
            )


        # If the word is in the index
        else:
            # index[word]['term frequency'] += 1

            # If the word has not been found in this document


            # print(index_word)
            temp = (index_word['info']['document(s)'])


            if doc_id not in temp.keys():

                index_word['info']['document frequency'] += 1

                index_word['info']['document(s)'][doc_id] =  {
                                                        'frequency' : 1,
                                                        'doc_id': doc_id
                                                      }


            # If the word has been found in this document
            else:
                index_word['info']['document(s)'][doc_id]['frequency'] += 1




            db[index_col_name].save(index_word)


    # return index




def store(index, index_col_name):
    #  for only dprocess database
    #  main document

    collection = db[index_col_name]


    for word in index:
        collection.save({'_id' : word, 'info' : index[word]})
    


def store_doc(files_collection,text):
    #  for only dprocess database
    #  main document
    collection = db[files_collection]
    id = collection.save({'data':text})
    print (id)

    return id



def store_doc_by_db(collection,text):

    id = collection.save({'data': text})
    print(id)

    return id


def store_by_db(index, collection):

    for word in index:
        collection.save({'_id': word, 'info': index[word]})