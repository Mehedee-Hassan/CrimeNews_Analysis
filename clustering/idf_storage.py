import sys, os

import clustering
import location

projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)


import lib.lib_cosine.parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient


# Indexing
startTime = time.time()
index = {}

# database collection settings
import db.CommonNames as CN

client = MongoClient()
db = CN.TestDb.getDatabase(client)
index_col_name = CN.TestDb.indexCollectionName()
document_col_name = CN.TestDb.documentCollectionName()


# ==============================


def save():
    startTime = time.time()

    files = [file for file in os.listdir(temp_crime_files) if os.path.isfile(temp_crime_files + "\\" + file)]


    # Iterate through every file

    print("debug##", len(files))

    numoffiles = 0
    for file in files:

        print("debug##",file)


        # Split the file in lines

        p = temp_crime_files + "\\"+file
        temp_doc = open(file=p,mode='r',encoding="utf-8").read()


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
        id = parsing.store_doc_by_db(collection=db[document_col_name], text=string)

        # Add the words to the index
        parsing.make_term_index_by_db(words=words, index=index,id=id,db=db,index_col_name=index_col_name)




    print("Indexation took " + str(time.time() - startTime) + " seconds.")

    # Storage
    startTime = time.time()
    parsing.store_by_db(index=index, collection=db[index_col_name])
    print("Storage took " + str(time.time() - startTime) + " seconds.")


if __name__ == '__main__':

    root_path = os.path.abspath('..')
    print("files in :",root_path)
    temp_crime_files = root_path + "\\temp_files\\crime"
    temp_n_crime_files = root_path + "\\temp_files\\ncrime"

    print(temp_crime_files)

    save()

else:
    root_path = os.path.abspath('.')
    print(root_path)
    temp_crime_files = root_path + "\\temp_files\\crime"
    temp_n_crime_files = root_path + "\\temp_files\\ncrime"