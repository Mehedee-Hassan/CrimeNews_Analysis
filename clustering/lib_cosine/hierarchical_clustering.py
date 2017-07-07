
import sys, os
from pprint import pprint

import math

projectpath = os.path.dirname(os.path.realpath('idf_storage.py'))
libpath = projectpath + '/lib_cosine'
sys.path.append(libpath)
os.chdir(projectpath)


import clustering.lib_cosine.parsing_cosine as parsing
import re
import time
import pymongo
from pymongo import MongoClient
from pqdict import pqdict
from clustering.lib_cosine.hierarchical_cluster_lib import HClust,DistanceMatrix
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
import queue

no_cluster = 'NC'

# ==============================


clusters = {}

def hierarchical(doc_list,min_limit_distance = 0.1):
    length = len(doc_list)

    distance_dic = localDistance(doc_list)

    distanceMat = DistanceMatrix(distance_dictionary=distance_dic,obs_list=doc_list)

    hc = HClust(distanceMat,linkage_criterion='min')

    # clusterlist = hc.n_clusters(7)
    # up to 10% matching documents
    clusterlist = hc.minimum_distance_cluster(min_limit_distance)

    # cut = hc.cut(3)
    # print(clusterlist)

    # pair_list = make_pair_init(distance_dic)



    # makeCluster(pair_list,doc_list)

    # makeCluster_old(distance_dic, doc_list)


    return clusterlist


# def makeCluster(pair_list,doc_list):
#     level = []
#     cluster_list = {}
#     temp_doc_list = doc_list
#     cluster_name  = 0
#     cluster_level = 0
#     matrix = {}
#
#
#     while pair_list.not_empty():
#
#         tuple = pair_list.get()
#
#         if tuple[2] != no_cluster:
#
#             cluster_list[cluster_name] = []
#             tuple[2] = cluster_name
#             cluster_list[cluster_name].append(tuple[1])
#             cluster_list[cluster_name].append(tuple[2])
#
#             matrix[cluster_name] = tuple[1]
#
#             isert(pair_list,tuple[1],cluster_name,temp_doc_list)
#
#             cluster_name += 1
#         else :
#
#             if tuple[3] not in cluster_list:
#                 cluster_list[tuple[3]] =[]
#
#             cluster_list[tuple[3]].append(tuple[2])
#
#
#
#
#         distance_from_cluster()



# def distance_from_cluster():

# def isert(pair_list,doc_id,name,temp_doc_list):
#
#     for key,val in temp_doc_list[doc_id]:
#         pair_list.put((val,doc_id,key,name))







# def make_pair_init(distance_dic):
#
#     pq = queue.PriorityQueue()
#
#
#     distance_dic_temp = distance_dic
#
#     for key,doc_dictionary in distance_dic_temp:
#
#         for id_key,distance in doc_dictionary:
#
#             # first document id = key and id = document id_key
#             # val = cosine distance between two document
#             # NC = not a cluster
#             pq.put((distance , key ,id_key,'NC'))
#
#
#             if id_key in distance_dic_temp:
#                 del distance_dic_temp[id_key][key]
#
#
#     return pq




def returnVect(documentID):

    tf_list = db[tfvectDoc_col_name].find_one({'_id': documentID})

    # print("not in list = ",documentID)



    tf_list = dict(tf_list['_normtf'])

    return tf_list




def cosine_distance(doc1 ,doc2,__emptyVect):




    if __emptyVect == True:

        # print("doc2 = ")
        # pprint(doc2)
        vect1 = (returnVect(doc1))
        vect2 = (returnVect(doc2))
        # pprint(vect2)

    else:
        vect1 = (returnVect(doc1))
        vect2 = doc2


    distance =0
    summationV = []
    # pprint(vect1)

    sum_v = 0

    for word,val in vect1.items():
        # if __emptyVect == True:
        #     print('key = ',word," ",val)


        if word in vect2:
            sum_v += round((vect1[word]*vect2[word]),4)


    return sum_v



def getDistanceFromSimilarity(simiScore):

    dist  = ((2*math.acos(simiScore))/ 3.141592)

    return dist

def localDistance(doc_list):

        distance = {}
        lenght = len(doc_list)

        for i in range(0,lenght):
            for j in range(i+1 ,lenght):

                if doc_list[i] not in distance:
                    distance[doc_list[i]] = {}

                if doc_list[j] not in distance:
                    distance[doc_list[j]] = {}

                # print('now =',i,' ',j)

                dist = cosine_distance(doc_list[i],doc_list[j],True)
                distance[doc_list[i]][doc_list[j]]=dist
                distance[doc_list[j]][doc_list[i]]=dist




        # for key ,val in distance.items():
        #     distance[key] = ((sorted(val.items(), key=lambda x: x[1],reverse=True)))




        # pprint(distance)

        return distance



# old unfinished make cluster


# def makeCluster_old(distance, doc_list):
#
#     max = 0.0
#
#     temp_dict = {}
#     taken = {}
#     cluster = {}
#     cls = 0
#     lenght = len(doc_list)
#     now  = {}
#
#     cl = []
#
#     for i in range(0, lenght):
#
#         if cls not in cluster:
#             cluster[cls] = {}
#         if doc_list[i] in taken:
#             taken[doc_list[i]] = {}
#
#
#         cluster[cls][doc_list[i]] = 2
#         taken[doc_list[i]][cls]  = 2
#
#         now[doc_list[i]] = cls
#
#         cl.append(cls)
#         cls+=1
#
#
#     b = 0
#     while True:
#
#         for i in range(0, lenght):
#
#            if i != lenght-1 and cl[i]!=cl[i+1]:
#
#                key = distance[doc_list[i]].keys()
#
#                for k in key:
#                    if cl[doc_list[i]] != cl[k]:
#
#                        dist_key = list(distance.keys())[0]
#
#                        if k == dist_key:
#                            now[dist_key] = now[doc_list[i]]
#
#                        else:
#
#
#                print(key[0]," ", list(distance.keys())[0])
#
#
#
#
#            print('now =', i, ' ', j)
#
#
#         b += 1
#         if b > 1000:
#             break







