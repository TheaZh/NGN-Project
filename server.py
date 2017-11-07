from flask import Flask
from pymongo import MongoClient
import Mongo
app = Flask(__name__)

# assignment.manager.ngn@gmail.com
# assignment.manager123
# mongoDB Cloud: mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system

# MongoDB URI - for normal collections
mongo_uri = "mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system"
client = MongoClient(mongo_uri)  # connect to MongoDB Cloud
db = client.get_default_database() # normal database -- storing normal info

# MongoDB URI - For files only
mongo_file_uri = "mongodb://assignment.manager:assignment.manager123@ds249575.mlab.com:49575/files-management"
file_client = MongoClient(mongo_file_uri)
file_db = client.get_default_database()  # file database -- storing assignment files

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
