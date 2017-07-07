import time

from bson import ObjectId
from pymongo import MongoClient

# Indexing
startTime = time.time()
index = {}



# database collection settings
import lib.lib_cosine.CommonNames as CN

client = MongoClient()
db = CN.getDatabase(client)
index_col_name = CN.indexCollectionName()
tfvectDoc_col_name = CN.tfvCollectionName()
document_col_name = CN.documentCollectionName()


# ==

cursor = db[index_col_name].find()

docs= {}
#
# for document in cursor:
#     d = document['info']['document(s)']
#     d2 = list(document['info']['document(s)'].keys())
#     # print(document)
#     print(d)
#
#     for element in d2:
#         if element not in docs:
#             docs[element] = {}
#
#         docs[element][document['_id']] = d[element]['frequency']


    # print(d2)
    # print("=======")



# pprint(docs)

e = 'a'
d = 'b'

# db['test'].insert_one({
#     e: {
#         d: 'frequency'
#     }
# })
#
# db['test'].insert_one({
#     '_id': 'werweiru82398jewjd',
#     '_tf': [{'a':12312},{'c':12312},{'b':12312}]
# })

# tt = db.test.find_one({'_id' : 'werweiru82398jewjd'})
# list = list(tt['_tf'])
#
# list.append({'m':546456})
#
# tt['_tf'] = list
#
# print (list)
#
# db['test'].update_one(
#     {'_id':tt['_id']},
#     {
#         "$set":{
#             '_tf': list
#         }
#     }
# )



docs2 = ["593868425b65ad3bc89b9405" ,
"593868455b65ad3bc89b9450",
"593868495b65ad3bc89b94c1",
"593868625b65ad3bc89b96fd","5938683d5b65ad3bc89b93b8","5938683d5b65ad3bc89b93b2","5938684c5b65ad3bc89b94fb","5938682f5b65ad3bc89b929b","5938683b5b65ad3bc89b9396","593868615b65ad3bc89b96dd","593868325b65ad3bc89b92e4","593868595b65ad3bc89b9613","593868595b65ad3bc89b9612","593868445b65ad3bc89b9448","5938682c5b65ad3bc89b924e","593868595b65ad3bc89b960a","5938685a5b65ad3bc89b9616","593868335b65ad3bc89b92f0","5938685a5b65ad3bc89b9617","593868275b65ad3bc89b91e4","593868345b65ad3bc89b9308","593868595b65ad3bc89b9610","593868595b65ad3bc89b9611","5938685a5b65ad3bc89b9615","593868285b65ad3bc89b91e6","593868345b65ad3bc89b9300","593868595b65ad3bc89b960f","593868595b65ad3bc89b960e","593868335b65ad3bc89b92f6","593868595b65ad3bc89b960b","593868325b65ad3bc89b92ec","593868345b65ad3bc89b92fe","593868595b65ad3bc89b960d","593868595b65ad3bc89b9609","593868245b65ad3bc89b919a"]

docs = ["593868345b65ad3bc89b9306",
"5938683d5b65ad3bc89b93b8",
"593868615b65ad3bc89b96db",
"5938682a5b65ad3bc89b9218",
"593868615b65ad3bc89b96dd",
"5938682f5b65ad3bc89b929b",
"593868325b65ad3bc89b92e9",
"593868345b65ad3bc89b92fe",
"593868445b65ad3bc89b9448",
"593868595b65ad3bc89b960b",
"593868505b65ad3bc89b954c",
"593868555b65ad3bc89b95b7",
"593868615b65ad3bc89b96d1",
"5938685a5b65ad3bc89b9617",
"593868375b65ad3bc89b9346",
"593868605b65ad3bc89b96c7",
"593868275b65ad3bc89b91db",
"5938685f5b65ad3bc89b96ab",
"593868285b65ad3bc89b91f3",
"593868355b65ad3bc89b930a",
"5938685a5b65ad3bc89b9615",
"593868335b65ad3bc89b92f1",
"593868595b65ad3bc89b960e",
"593868275b65ad3bc89b91d4",
"593868595b65ad3bc89b960c",
"593868595b65ad3bc89b960a",
"593868315b65ad3bc89b92c7",
"593868595b65ad3bc89b960f",
"5938682b5b65ad3bc89b923c",
"593868595b65ad3bc89b960d",
"593868595b65ad3bc89b9609"]
dd = ['593aff055b65ad2020708dc4', '593aff105b65ad2020708de4', '593afd935b65ad2020708937', '593afdf55b65ad2020708a92', '593aff065b65ad2020708dc5', '593afefe5b65ad2020708db2', '593aff005b65ad2020708db8', '593aff015b65ad2020708dba', '593afe295b65ad2020708b2f', '593afec55b65ad2020708cfd', '593afec45b65ad2020708cfa', '593afec35b65ad2020708cf7', '593afec45b65ad2020708cf9', '593aff045b65ad2020708dc2', '593afec45b65ad2020708cfb', '593afef55b65ad2020708d96', '593afefd5b65ad2020708dae', '593afefd5b65ad2020708db0', '593afeb75b65ad2020708cd3', '593afec05b65ad2020708cf2', '593afec45b65ad2020708cf8', '593afec25b65ad2020708cf5', '593afec15b65ad2020708cf4', '593afec35b65ad2020708cf6', '593afec55b65ad2020708cfc', '593afef45b65ad2020708d92', '593afebf5b65ad2020708cf1', '593afec05b65ad2020708cf3', '593afebf5b65ad2020708cf0', '593afec55b65ad2020708cfe']
for d in dd:
   t =  db.documents.find_one({'_id': ObjectId(d)})

   print(t)


# insert vs save

# db['test_insert'].insert({'test5':32847923})
# db['test_insert'].insert({'test6':32847923})
# db['test_insert'].insert({'test7':32847923})
# db['test_insert'].insert({'test8':32847923})



# def nltkTockenizer(string):
#     tokenizer = RegexpTokenizer(r'\w+')
#
#     tokens = tokenizer.tokenize(string)
#     tokens = [token.lower() for token in tokens]
#
#     engStem  =snowballstemmer.stemmer('english')
#     englishStopWords = stopwords.words('english')
#
#     tokens = [engStem.stemWord(token) for token in tokens]
#     tokens = [token for token in tokens if token not in englishStopWords]
#
#
#     return tokens
#
#
# data = "this is a line" \
#        "\n\n\nthis is another line" \
#        "\nlakjsd ladjflk asjdflka jsdlfkjsalkdf jlskdj flksjd flkajsd flkja sdf" \
#        "\nksldfjksdfjlksdf lsakdjf lakj 2j4398273 rswjenkjs r83u2 ewrn sh 1k2l31 '\sdfk jsldkfj"
#
# aa = nltkTockenizer(data)
#
# print(aa)