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

    # return isGrader
    res = {
        'isGrader': data['isGrader'],
        'uni': data['uni']
    }
    return jsonify(res)

@app.route('/student_system/<userUNI>')
def student(userUNI):
    user_uni = userUNI
    user = db['User']
    user_data = user.find_one({'uni':user_uni})
    user_data.pop('_id')
    # print 'user_data ---', user_data
    courses_list = user_data['course_list']
    courses_data = []
    course = db['Course']
    for one in courses_list:
        # one == course_id
        tmp_course_data = course.find_one({'course_id':one})
        tmp_course_data.pop('_id')
        courses_data.append(tmp_course_data)
    # print 'all course -- ', courses_data
    user_course = [user_data, courses_data]
    return jsonify(user_course)
    # data = request.get_data()
    # print data
    # data = request.args.get('student_data')
    # student_data = json.loads(data)
    # course_list = student_data['course_list']
    # # print course_list
    # course = db['Course']
    # courses_data = []
    # for course_id in course_list:
    #     cour = course.find_one({'course_id': course_id})
    #     cour.pop('_id')
    #     courses_data.append(cour)
    # # print courses_data
    # return jsonify(courses_data)
    # # return redirect('/show_student')

@app.route('/show_student/<userUNI>')
def show(userUNI):
    user_uni = json.loads(userUNI)['uni']
    # print user_uni
    return render_template('student-page.html', user_uni = user_uni)

@app.route('/get_grade/<course_id>/<uni>')
def get_grade(course_id,uni):
    course = db['Course']
    assignment = db['Assignment']
    assignment_list = sorted(course.find_one({'course_id':course_id})['assignment_list'])
    # data = []
    grade = dict()
    for assign_id in assignment_list:
        assign_data = assignment.find_one({'assignment_id': assign_id})
        grade_dict = assign_data['grade_dict']
        print 'grade_dice: ', grade_dict
        grade[assign_id] = []
        if uni in grade_dict:
            grade[assign_id] = grade_dict[uni]
    print grade
    return jsonify(grade)



if __name__ == '__main__':
    app.debug = True
    app.run()
