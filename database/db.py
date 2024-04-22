from pymongo import MongoClient

class Database(object):
    def __init__(self, dataBaseName = None, connectionString = None):
        
        if ((dataBaseName == None) or ( connectionString == None)):
            raise Exception('The Mongo DB dataBaseName and connectionString properties are undefined!')

        self.__dataBaseName = dataBaseName
        self.__connectionString = connectionString
        self.__dbConnection = None    
        self.__dataBase = None

    @property
    def dataBase(self):
            return self.__dataBase

    @property
    def dbConnection(self):
        return self.__dbConnection


    def connect(self) -> bool:
        try:
            self.__dbConnection = MongoClient(self.__connectionString)
            dbName = str(self.__dataBaseName)
            self.__dataBase = self.__dbConnection[dbName]
            return True
        except Exception as e:
            print(f"(?) MongoDB.connect Exception \n {e}")
            return False





