
import sys, os
from pprint import pprint

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
tfvectDoc_col_name = CN.tfvCollectionName()
document_col_name = CN.documentCollectionName()


# ==============================






def returnVect(documentID):

    tf_list = db[tfvectDoc_col_name].find_one({'_id': documentID})

    # print("not in list = ",documentID)



    tf_list = dict(tf_list['_normtf'])

    return tf_list




def cosine_distance(doc1 ,doc2
                    # avg_vect,avg_count_vect
                    # ,vect1
                    # ,vect2
                    ,__emptyVect):

    vect1 = {}
    vect2 = {}



    if __emptyVect == True:

        print("doc2 = ")
        pprint(doc2)
        vect1 = (returnVect(doc1))
        vect2 = (returnVect(doc2))
        pprint(vect2)

    else:
        vect1 = (returnVect(doc1))
        vect2 = doc2






    distance =0
    summationV = []
    # pprint(vect1)

    sum_v = 0

    for word,val in vect1.items():
        if __emptyVect == True:
            print('key = ',word," ",val)

        # mean vector save
        # if word not in avg_vect:
        #     avg_vect[word] = 0
        #     avg_count_vect[word] =0
        #
        #
        # avg_vect[word] += val
        # avg_count_vect[word] +=1

        if word in vect2:
            # print('word = ',word ,"\n", vect2[word])

            sum_v += round((vect1[word]*vect2[word]),3)



    return sum_v


def main():

    avg_vect = {}
    avg_count_vect = {}
    distance = cosine_distance('593afec55b65ad2020708cfe','593afec55b65ad2020708cfe',
    True)


    # print (avg_vect)
    print ("distance = ",distance)

# main()




ClusterA = 1
ClusterB = 2


def k_means(document_list):

    l = len(document_list)-1

    l2= int(l/2)

    first_mean = document_list[0]
    second_mean = document_list[l]

    cluster = {}
    distance_from_mean = {}

    avg_vect = {}
    avg_count_vect = {}

    __emptyVect = True

    meanA={}
    meanB={}


    oldA = {}
    oldB = {}
    oldCluster = {}


    terminate  = 0
    while True:

        for doc in document_list:


            distance1 = cosine_distance(doc , first_mean

                                        ,__emptyVect)

            distance2 = cosine_distance(doc , second_mean

                                        ,__emptyVect)

            if distance1 > distance2:
                cluster[doc] = ClusterA
                distance_from_mean[doc] = distance2
            else:
                cluster[doc] = ClusterB
                distance_from_mean[doc] = distance1


        first_mean ,second_mean = meanVector(cluster,distance_from_mean)

        __emptyVect = False

        _changeFlag = cluserChanged(cluster,oldCluster)

        if _changeFlag == False:
            break


        oldCluster = cluster

        terminate += 1
        if terminate > 1000:
            print("breked ")
            break



    for key,val in cluster.items():
        print("doc = ",key,'cluster= ',val)




def cluserChanged(cluster,oldCluster):

    if len(oldCluster) <=0:
        return True

    for key,val in cluster.items():
        if cluster[key] != oldCluster[key]:
            return True


    return False







def avg_vector(cluser,distance_from_mean):

    meanCluserA = {}
    meanCluserACnt = {}

    meanCluserB = {}
    meanCluserBCnt = {}


    print("k means 1 " ,"cluster = ",cluser)

    for key ,val in cluser.items():

        if val  == ClusterA:
            word_vector = returnVect(key)

            for word ,tfnorm in word_vector.items():

                if word not in meanCluserA:
                    meanCluserA[word] = 0
                    meanCluserACnt[word] = 0

                # print("k_means2" , word ," transform",tfnorm)

                meanCluserA[word] += float(tfnorm)
                meanCluserACnt[word] += 1

        if val  == ClusterB:
            word_vector = returnVect(key)

            for word ,tfnorm in word_vector.items():

                if word not in meanCluserB:
                    meanCluserB[word] = 0
                    meanCluserBCnt[word] = 0

                meanCluserB[word] += tfnorm
                meanCluserBCnt[word] += 1


        for key ,val in meanCluserA.items():
            meanCluserA[key] = round((meanCluserA[key] / meanCluserACnt[key]),3)

        for key ,val in meanCluserB.items():
            meanCluserB[key] = round((meanCluserB[key] / meanCluserBCnt[key]),3)




    return meanCluserA,meanCluserB



def meanVector(cluser,distance_mean):
    a = {}
    b = {}

    for key ,val in cluser.items():

        if val == ClusterA:
            a[key] = distance_mean[key]
        else:
            b[key] = distance_mean[key]

    a = sorted(a.items(), key=lambda x: x[1])
    b = sorted(b.items(), key=lambda x: x[1])

    len_a = int(len(a)/2)
    len_b = int(len(b)/2)

    print(a)

    a_vect = returnVect(a[len_a][0])
    b_vect = returnVect(b[len_b][0])

    return a_vect,b_vect