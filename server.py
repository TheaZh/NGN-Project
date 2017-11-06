from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# assignment.manager.ngn@gmail.com
# assignment.manager123
# mongoDB Cloud: mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system

mongo = "mongodb://assignment.manager:assignment.manager123@ds161873.mlab.com:61873/assignment-management-system"

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
