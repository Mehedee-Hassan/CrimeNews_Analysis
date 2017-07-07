from bson import ObjectId

import db.CommonNames as CN

from pymongo import MongoClient

client = MongoClient()
db = CN.RawDb.getDatabase(client)

idlist = db[CN.RawDb.getOnlineCollection()].findOne({'_id': ObjectId('595f09df5b65ad1684cee395')})


for a in idlist:
    print(a['text'])