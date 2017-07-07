from bson import ObjectId

import db.CommonNames as CN

from pymongo import MongoClient


class Retrieve:


    def __init__(self):
        self.client = MongoClient()
        self.testDb = CN.TestDb.getDatabase(self.client)
        self.rawDb = CN.RawDb.getDatabase(self.client)


    def getTotalData(self):
        num = self.rawDb[CN.RawDb.getNewsIndexCollection()].find({}).count()
        return num

    def getTotalDataIndex(self):

        idlist = self.rawDb[CN.RawDb.getNewsIndexCollection()].find({})

        return idlist



    def notInDocument(self,id):

        if self.testDb[CN.TestDb.documentCollectionName()].find({}).count() > 0:
            return False

        return True


    def getData(self,id):
        idlist = self.rawDb[CN.RawDb.getNewsIndexCollection()].find({'_id':ObjectId(id)})
