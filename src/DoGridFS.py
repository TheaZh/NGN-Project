from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import *

# file Database - GridFS
GRIDFS_URI = "mongodb://assignment:assignment123@ds249575.mlab.com:49575/files-management"
GF = MongoClient(GRIDFS_URI)
FILE_DB = GF['files-management']

def insert_file(file_name, user_uni):
    # conncet to a specific collection
    # collection name is user's UNI
    fs = GridFS(FILE_DB, user_uni)
    with open(file_path.decode('utf-8'), 'rb') as myfile: # read as binary format
        data = myfile.read()
        id = fs.put(data, filename=self.file_name)
        print id
    if not keep_org_file:
        gz_path = "./"+self.gz_name
        os.remove(gz_path)
