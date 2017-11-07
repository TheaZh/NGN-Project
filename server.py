from flask import Flask, render_template, request, redirect, url_for,jsonify
import json
from pymongo import MongoClient

# normal MongoDB
mongo_uri = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
client = MongoClient(mongo_uri)
db = client['assignment-management-system']


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/login')
def login():
    user_pass = request.args # contains user's uni and password

    uni = user_pass.get('uni')
    password = user_pass.get('password')

    user = db['User']
    data = user.find_one({'uni': uni, 'password': password})

    # no such user or password is not correct
    if not data:
        error_msg = 'No such user or password is not correct!'
        return jsonify({'error_msg': 'No such user or password is not correct!'})

    # reomove '_id' attribute from result data
    if '_id' in data:
        data.pop('_id')

    # check if the current user is grader or student
    if not data['isGrader']: # is a student
        # result = json.dumps(data)
        return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
