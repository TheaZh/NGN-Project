from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
import json, os, datetime, time, sys, tarfile, shutil
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from gridfs import *
from bson.objectid import ObjectId


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


@app.route('/grader_system')
def grader():
    user_data = USER.find_one({'uni': session['uni']})
    user_data.pop('_id')

    courses_list = user_data['course_list']
    courses_data = []
    for one in courses_list:
        # one == course_id
        tmp_course_data = COURSE.find_one({'course_id': one})
        tmp_course_data.pop('_id')
        courses_data.append(tmp_course_data)

    user_course = [user_data, courses_data]
    return jsonify(user_course)


@app.route('/grader_view')
def grader_view():
    assignment = ASSIGNMENT.find_one({'assignment_id': request.args.get('assignment_id')})
    grade_dict = assignment['grade_dict']
    return jsonify(grade_dict)


@app.route('/show_student/<userUNI>', methods=['POST', 'GET'])
def show(userUNI):
    user_uni = json.loads(userUNI)['uni']
    # print user_uni
    return render_template('student-page.html', user_uni=user_uni)


@app.route('/show_grader')
def show_grader():
    return render_template('grader-page.html', user_uni=session['uni'])


@app.route('/post')
def post_grade():
    grade = []
    grade_dict = {}
    grade.append(request.args.get('grade'))
    grade.append(request.args.get('comment'))
    grade_dict[request.args.get('uni')] = grade

    ASSIGNMENT.update_one(
        {'assignment_id': request.args.get('assignment_id')},
        {
            "$set": {
                'grade_dict': grade_dict
            }
        }
    )

    return jsonify(' ')


@app.route('/add_assignment')
def add_assignment():
    course_id=request.args.get('course_id')
    description=request.args.get('description')
    data = COURSE.find_one({'course_id': course_id})
    length = len(data['assignment_list'])
    assignment_id = course_id + '_A' + str(length + 1)
    data['assignment_list'].append(assignment_id)
    # update assignment_collection
    new_assignment = {'assignment_id': assignment_id,
                      'description': description,
                      'submitted_file_dict': {},
                      'upload_file_dict': {},
                      'grade_dict': {}
                      }
    ASSIGNMENT.insert(new_assignment)
    # update course course_collection
    COURSE.update_one({'course_id': course_id}, {'$set': data})
    return jsonify('')


@app.route('/download_file/<uni>/<assignment_id>')
def download(uni, assignment_id):
    clean_tmp()
    # uni = request.args.get('uni')
    # assignment_id = request.args.get('assignment_id')
    assignment = ASSIGNMENT.find_one({'assignment_id': assignment_id})
    file_ids_list = assignment['submitted_file_dict'][uni][0]
    # submitted_file_dict{uni : [ [file ids], timestamp ] }
    print 'file_ids_list:', file_ids_list
    user_file_collection = GridFS(FILE_DB, uni)
    os.chdir(sys.path[0])
    dir_name = assignment_id + '_' + uni
    download_path = os.path.join("./tmp/download", dir_name)
    print 'download_path: --- ', download_path
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    for file_id in file_ids_list:
        print "file_id --- ", file_id
        file_db = user_file_collection.get(ObjectId(file_id))
        file_path = os.path.join(download_path, file_db.filename)
        file_io = open(file_path, "wb")
        file_io.write(file_db.read())
        file_io.close()
    print("Success")
    file_download = dir_name + '.tar.gz'
    make_targz(download_path, download_path)
    return send_from_directory("./tmp/download", file_download, as_attachment=True)


def make_targz(file, source_dir):
        gz_name = file + ".tar.gz"
        with tarfile.open(gz_name, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))


@app.route('/get_grade')
def get_grade():
    para = request.args

    course_id = para.get('course_id')
    uni = para.get('uni')

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
    print('get_assignment parameters: ', para)
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
    # Get file id list
    file_ids_list = json.loads(request.args.get('file_ids_list'))
    print file_ids_list
    # access to GridFS collection -- collection name is studetn uni
    cur_user_uni = session['uni']
    cur_assignment_id = session['assignment_id']
    user_FS_collection_name = cur_user_uni
    user_FS_collection = GridFS(FILE_DB, user_FS_collection_name)
    # build file name dict -- key: filename_version, value: file_id('_id')
    file_name_dict = {}
    if file_ids_list:
        for file_id in file_ids_list:
            tmp_file_data = user_FS_collection.find_one({'_id': ObjectId(file_id)})
            tmp_file_name = tmp_file_data.filename
            tmp_file_version = tmp_file_data.version
            file_name = tmp_file_name + '-' + str(tmp_file_version)
            file_name_dict[file_name] = [file_id, tmp_file_data.timestamp]

    return jsonify(file_name_dict)


def allowed_file(filename):
    # constraint the allowed extensions of uploading files
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            os.remove(tmp_file_path)
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
        ts = time.time()
        display_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        id = user_FS_collection.put(data, filename=file_name, version = version_count, assignment_id = cur_assignment_id, timestamp = display_time)
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


@app.route('/submit_files')
def submit_files():
    submit_id_list = json.loads(request.args.get('submit_id_list'))
    print('submit_id_list:', submit_id_list)
    cur_user_uni = session['uni']
    cur_assignment_id = session['assignment_id']
    # timestamp for submission
    ts = time.time()
    display_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # no file chosen to submit
    if len(submit_id_list) == 0:
        return jsonify({'msg':'NoFile'})

    assignment_info = ASSIGNMENT.find_one({'assignment_id': cur_assignment_id})
    submitted_file_dict = assignment_info['submitted_file_dict']
    # first item is the file id list, second item is the timestamp for submission
    new_sub_list = []
    new_sub_list.append(submit_id_list)
    new_sub_list.append(display_time)
    submitted_file_dict[cur_user_uni] = new_sub_list
    ASSIGNMENT.update_one({'assignment_id': cur_assignment_id},
                          {'$set': {
                              "submitted_file_dict": submitted_file_dict
                          }})
    print('update submit: ',ASSIGNMENT.find_one({'assignment_id': cur_assignment_id}))
    return jsonify({'msg': 'FileSubmitted'})


@app.route('/get_submitted_files')
def get_submitted_files():
    submitted_file_ids = json.loads(request.args.get('submitted_file_ids'))
    print('submitted_file_ids: ', submitted_file_ids)
    cur_user_uni = session['uni']
    cur_assignment_id = session['assignment_id']
    user_FS_collection_name = cur_user_uni
    user_FS_collection = GridFS(FILE_DB, user_FS_collection_name)
    # build file name dict -- key: filename_version, value: file_id('_id')
    submitted_file_name_dict = {}
    if submitted_file_ids:
        for file_id in submitted_file_ids:
            print('each file id submit -- ', file_id)
            tmp_file_data = user_FS_collection.find_one({'_id': ObjectId(file_id)})
            tmp_file_name = tmp_file_data.filename
            tmp_file_version = tmp_file_data.version
            file_name = tmp_file_name + '-' + str(tmp_file_version)
            submitted_file_name_dict[file_name] = file_id
    return jsonify(submitted_file_name_dict)


@app.route('/delete_files')
def delete_files():
    delete_id_list = json.loads(request.args.get('delete_id_list'))
    print('Delete:', delete_id_list)

    cur_assignment_id = session['assignment_id']
    cur_user_uni = session['uni']
    user_FS_collection_name = cur_user_uni
    user_FS_collection = GridFS(FILE_DB, user_FS_collection_name)

    assignment_info = ASSIGNMENT.find_one({'assignment_id': cur_assignment_id})
    upload_file_dict = assignment_info['upload_file_dict']
    submitted_file_dict = assignment_info['submitted_file_dict']
    cur_user_submitted = []
    if cur_user_uni in submitted_file_dict:
        cur_user_submitted = submitted_file_dict[cur_user_uni][0]
        print 'cur_user_submitted: ', cur_user_submitted
    msg = ''
    for delete_id in delete_id_list:
        if delete_id in cur_user_submitted:
            msg = 'Some files cannot be deleted, because they have been already submitted.'
            print msg
            print 'Skipped ----- ', delete_id
            continue
        upload_file_dict[cur_user_uni].remove(delete_id)
        user_FS_collection.delete(ObjectId(delete_id))
        print 'Deleted ---- ', delete_id
    ASSIGNMENT.update_one({'assignment_id': cur_assignment_id},
                          {'$set': {
                              "upload_file_dict": upload_file_dict
                          }})
    return jsonify({'msg': msg})


@app.route('/download_from_cloud/<object_id>')
def download_from_cloud(object_id):
    clean_tmp()
    cur_user_uni = session['uni']
    user_FS_collection_name = cur_user_uni
    user_FS_collection = GridFS(FILE_DB, user_FS_collection_name)
    os.chdir(sys.path[0])
    if not os.path.exists("./tmp/download"):
        os.mkdir("./tmp/download")
    file_db = user_FS_collection.get(ObjectId(object_id))
    file_path = os.path.join("./tmp/download", file_db.filename)
    file_io = open(file_path, "wb")
    file_io.write(file_db.read())
    file_io.close()
    print("Success")
    return send_from_directory("./tmp/download", file_db.filename, as_attachment=True)


def clean_tmp():
    os.chdir(sys.path[0])
    if os.path.exists("./tmp/download"):
        shutil.rmtree('./tmp/download')
    os.mkdir('./tmp/download')


if __name__ == '__main__':
    app.secret_key = "this_is_an_NGN_project"
    app.debug = True
    app.run()
