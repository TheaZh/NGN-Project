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

    return jsonify(data)

@app.route('/student_system')
def student():
    data = request.args
    student_data = json.loads(data.get('student_data'))
    course_list = student_data['course_list']
    print course_list
    course = db['Course']
    courses_data = []
    for course_id in course_list:
        cour = course.find_one({'course_id': course_id})
        cour.pop('_id')
        courses_data.append(cour)
    print courses_data
    return jsonify(courses_data)




if __name__ == '__main__':
    app.debug = True
    app.run()
