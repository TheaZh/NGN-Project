from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json, os
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from gridfs import *


# normal MongoDB
MONGO_URI = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
client = MongoClient(MONGO_URI)
db = client['assignment-management-system']
USER = db['User']
COURSE = db['Course']
ASSIGNMENT = db['Assignment']

# file Database - GridFS
GRIDFS_URI = "mongodb://assignment:assignment123@ds249575.mlab.com:49575/files-management"
GF = MongoClient(GRIDFS_URI)
FILE_DB = GF['files-management']

CACHE = './tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('login.html')


@app.route('/login')
def login():
    user_pass = request.args  # contains user's uni and password

    uni = user_pass.get('uni')
    password = user_pass.get('password')

    data = USER.find_one({'uni': uni, 'password': password})

    # no such user or password is not correct
    if not data:
        error_msg = 'No such user or password is not correct!'
        return jsonify({'error_msg': 'No such user or password is not correct!'})

    # return isGrader
    res = {
        'isGrader': data['isGrader'],
        'uni': data['uni']
    }
    session['uni'] = data['uni']
    return jsonify(res)


@app.route('/student_system/<userUNI>')
def student(userUNI):
    user_uni = userUNI

    user_data = USER.find_one({'uni': user_uni})
    user_data.pop('_id')
    # print 'user_data ---', user_data

    courses_list = user_data['course_list']
    courses_data = []
    for one in courses_list:
        # one == course_id
        tmp_course_data = COURSE.find_one({'course_id': one})
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


@app.route('/show_student/<userUNI>', methods=['POST', 'GET'])
def show(userUNI):
    user_uni = json.loads(userUNI)['uni']
    # print user_uni
    return render_template('student-page.html', user_uni=user_uni)


@app.route('/get_grade')
def get_grade():
    para = request.args
    # print para
    course_id = para.get('course_id')
    uni = para.get('uni')
    # print 'course ID: ', course_id
    # print 'UNI: ', uni

    course_info = COURSE.find_one({'course_id': course_id})
    course_info.pop('_id')

    grader_uni = course_info['grader_id']
    grader_name = USER.find_one({'uni': grader_uni})['name']

    assignment_list = sorted(course_info['assignment_list'])
    # print 'assign list: ', assignment_list
    # data = []
    grade = dict()
    for assign_id in assignment_list:
        assign_data = ASSIGNMENT.find_one({'assignment_id': assign_id})
        grade_dict = assign_data['grade_dict']
        # print 'grade_dice: ', grade_dict
        grade[assign_id] = []
        if uni in grade_dict:
            grade[assign_id] = grade_dict[uni]
    # print grade
    data = {
        'grade': grade,
        'course_info': course_info,
        'grader': grader_name
    }
    # print 'data', data
    return jsonify(data)


@app.route('/get_assignment')
def get_assignment():
    para = request.args
    # print('get_assignment parameters: ', para)
    # course_id = para.get('course_id')
    assignment_id = para.get('assignment_id')
    session['assignment_id'] = assignment_id
    # print(session['assignment_id'])
    assignment_info = ASSIGNMENT.find_one({'assignment_id': assignment_id})
    assignment_info.pop('_id')
    # print(assignment_info)
    return jsonify(assignment_info)



@app.route('/get_uploaded_files')
def get_uploaded_files():
    # NOT finished Yet
    file_ids_list = request.args.get('file_ids_list')


def allowed_file(filename):
    # constraint the allowed extensions of uploading files
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/choose_files', methods=['GET', 'POST'])
def choose_files():
    return False


@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
    response_data = {
        'msg': ''
    }
    if request.method == 'POST':
        print('LET US UPLOAD!!!!')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            response_data['msg'] = 'No file part. Error!'

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            response_data['msg'] = 'Please Select a File.'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tmp_file_path = os.path.join(os.path.abspath(CACHE), filename)
            file.save(tmp_file_path)
            # return redirect(request.url)
            print("UPLOADED! -- filename: ", filename)
            response_data['msg'] = 'Successful Uploaded!'
            # remove local tmp file
            # os.remove(tmp_file_path)
            files_to_GridFS(tmp_file_path, filename)

    return jsonify(response_data)


def files_to_GridFS(file_path, file_name):
    cur_user_uni = session['uni']
    cur_assignment_id = session['assignment_id']
    user_FS_collection_name = cur_user_uni
    # access to GridFS collection -- collection name is studetn uni
    user_FS_collection = GridFS(FILE_DB, user_FS_collection_name)

    # count the number of versions that have been already submitted to GridFS
    version_count = 0
    for grid_out in user_FS_collection.find({'filename':file_name}):
        version_count = version_count + 1
    version_count = version_count + 1
    # put file in GridFS collection
    file_id = ''
    with open(file_path, 'rb') as MY_FILE:  # read as binary format
        data = MY_FILE.read()
        # # # # # # # # #
        # filename = file_name
        # version = the number of file with same name
        # assignment_id = cur_assignment_id
        id = user_FS_collection.put(data, filename=file_name, version = version_count, assignment_id = cur_assignment_id)
    # get the _id of this file
    file_id = str(id)
    # update Assignment collection
    assignment_info = ASSIGNMENT.find_one({'assignment_id': cur_assignment_id})
    upload_file_dict = assignment_info['upload_file_dict']
    # print('upload_file_dict:--', upload_file_dict)
    if cur_user_uni not in upload_file_dict:
        upload_file_dict[cur_user_uni] = []
    upload_file_dict[cur_user_uni].append(file_id)
    assignment_info['upload_file_dict'] = upload_file_dict
    # print('assignment_info: -- ', assignment_info)
    ASSIGNMENT.update_one({'assignment_id': cur_assignment_id},
                          {'$set': {
                              "upload_file_dict": upload_file_dict
                          }})
    assignment_info = ASSIGNMENT.find_one({'assignment_id': cur_assignment_id})







if __name__ == '__main__':
    app.secret_key = "this_is_an_NGN_project"
    app.debug = True
    app.run()
    # upload_files()
