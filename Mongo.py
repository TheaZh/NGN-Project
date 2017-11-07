from pymongo import MongoClient

# mLab
# assignment.manager.ngn@gmail.com
# assignment.manager123
# mongoDB Cloud: mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system

class Mongo:
    # MongoDB URI - for normal collections
    mongo_uri = "mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system"

    # MongoDB URI - For files only
    mongo_file_uri = "mongodb://assignment.manager:assignment.manager123@ds249575.mlab.com:49575/files-management"

    def connect_DB(self):
        self.client = MongoClient(mongo_uri)  # connect to MongoDB Cloud
        self.db = client.get_default_database() # normal database -- storing normal info
        return self.db

    def connect_GridFS(self):
        self.file_client = MongoClient(mongo_file_uri)
        self.file_db = client.get_default_database()  # file database -- storing assignment files
        return self.file_db

    def close_DB(self):
        self.client.close()

    def close_GridFS(self):
        self.file_client.close()
