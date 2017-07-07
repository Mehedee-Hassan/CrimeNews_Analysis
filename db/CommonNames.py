



class ProcessDb:
    def __init__(self):
        pass


    @staticmethod
    def getDatabase(client):
        return client.Crime_News_DB
        # return client.Crime_News_DB_temp

    @staticmethod
    def indexCollectionName():
        return 'index'

    @staticmethod
    def documentCollectionName():
        return 'documents'

    @staticmethod
    def tfvCollectionName():
        return 'tf_doc_vector'








class RawDb:

    def __init__(self):
        pass

    @staticmethod
    def getDatabase(client):
        return client.Crime_Raw_DB

    @staticmethod
    def getNewsIndexCollection():
        return 'online_news_index'

    @staticmethod
    def getOnlineCollection():
        return 'online_news'




class TestDb:
    @staticmethod
    def getDatabase(client):
        return client.testdb
        # return client.Crime_News_DB_temp

    @staticmethod
    def indexCollectionName():
        return 'index'

    @staticmethod
    def documentCollectionName():
        return 'documents'

    @staticmethod
    def tfvCollectionName():
        return 'tf_doc_vector'
