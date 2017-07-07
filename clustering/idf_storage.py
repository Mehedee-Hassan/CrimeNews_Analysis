import sys, os
projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)


import parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient


# Indexing
startTime = time.time()
index = {}



# database collection settings
import CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================



# Indicate the path where relative to the collection
os.chdir(projectpath + '/data/dailystar/crime/')
# os.chdir(projectpath + '/data/dailystar/story/7murder')
# os.chdir(projectpath + '/data/dailystar/story/tonu_rape')
# D:\programming\python\search_engine_test\mongodb\cosine_ranking\test1\data\dailystar\story\7murder
# os.chdir(projectpath + '/data_temp/')


# os.chdir(projectpath + '/data/' + files_collection)
# List all files in the collection
files = [file for file in os.listdir('.') if os.path.isfile(file)]
# Iterate through every file

numoffiles = 0
for file in files:
    # Split the file in lines

    temp_doc = open(file=file,mode='r',encoding="utf-8").read()


    lines_string = (temp_doc.split('\n'))

    string =''
    for l in lines_string:
        string = string +' '+l

    numoffiles +=1
    print("num = ",numoffiles,"lines = ")

    # data = temp_doc.splitlines()
    # Normalize the content
    words = parsing.clean_lines(lines_string)
    # Remove the extension from the file for storage
    # name = re.match('(^[^.]*)', file).group(0)


    # store documents
    id = parsing.store_doc(document_col_name, string)

    # Add the words to the index
    parsing.make_term_index(words, index,id)




print("Indexation took " + str(time.time() - startTime) + " seconds.")

# Storage
startTime = time.time()
parsing.store(index, index_col_name)
print("Storage took " + str(time.time() - startTime) + " seconds.")
