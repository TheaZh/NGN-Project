from pymongo import MongoClient
from Course import Course

class Assignment:
    def __init__(self):
        self.mongo_uri = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['assignment-management-system']
        self.assignment_collection = self.db['Assignment']

    # insert fake data - not used during program process
    def insert_assignments(self, seed_data):
        self.assignment_collection.insert_many(seed_data)

    # add a new assignment when grader published one
    def add_assignment(self, course_id, description):
        course = Course()
        data = course.course_collection.find_one({'course_id': course_id})
        length = len(data['assignment_list'])
        assignment_id = course_id + '_A' + str(length + 1)
        data['assignment_list'].append(assignment_id)
        # update assignment_collection
        new_assignment = {'assignment_id': assignment_id,
                'description': description,
                'submitted_file_dict': {},
                'upload_file_dict':{},
                'grade_dict': {}
                }
        self.assignment_collection.insert(new_assignment)
        # update course course_collection
        course.add_assignment(course_id, data)

    def close_DB(self):
        self.client.close()

if __name__ == '__main__':
    assignment_data = [
        {'assignment_id': 'COMS6111_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.1, 1.3, 1.12',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS6111_A2',
        'description': 'Textbook Chapter 1\n Excercise: 1.5, 1.8, 1.20',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS6111_A3',
        'description': 'Textbook Chapter 2\n Excercise: 2.4, 2.8, 2.17',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.13, 1.18, 1.24',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A2',
        'description': 'Textbook Chapter 3\n Excercise: 3.5, 3.3, 3.15',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A3',
        'description': 'Textbook Chapter 4\n Excercise: 4.9, 4.6, 4.7, 4.12, 4.13',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.7, 1.17, 1.27',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A2',
        'description': 'Textbook\n Chapter 2\t Excercise: 2.1, 2.3\n Chapter3\t Excercise: 3.30',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A3',
        'description': 'Textbook Chapter 4\n Excercise: 4.9, 4.6, 4.7, 4.12, 4.13',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS1234_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.9, 1.10, 1.21',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN5567_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.5, 1.12, 1.24',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN4377_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.18, 1.27',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4396_A1',
        'description': 'Textbook Chapter 1\n Excercise: 1.3, 1.18, 1.23',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        }
    ]
    assig = Assignment()
    # assig.insert_assignments(assignment_data)
    # assig.close_DB()
    # assig.add_assignment('COMS4396','Textbook Chapter 2\n Excercise: 2.8, 1.17, 1.34')
