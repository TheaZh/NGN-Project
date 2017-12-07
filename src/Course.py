from pymongo import MongoClient

'''
#### Example Course Schema ####

{
    "_id": {
        "$oid": "5a014a7962d4683f76c1626a"
    },
    "course_id": "COMS4396",
    "course_name": "Introduction to System Design",
    "assignment_list": [
        "COMS4396_A1"
    ],
    "grader_id": "xz1332"
}


course = {
    'course_id' : course_id,
    'course_name': course_name,
    'assignment_list': assignment_list,
    'grader_id': grader_id
         }



'''

class Course:
    def __init__(self):
        self.mongo_uri = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['assignment-management-system']
        self.course_collection = self.db['Course']

    # not used during programming process
    def insert_course(self, course_id, course_name, assignment_list, grader_id):
        seed_data = {'course_id' : course_id,
                    'course_name': course_name,
                    'assignment_list': assignment_list,
                    'grader_id': grader_id
                    }
        self.course_collection.insert(seed_data)

    # not used during programming process
    def insert_many_courses(self, seed_data):
        self.course_collection.insert_many(seed_data)

    # when grader publishes one new assignment, use this method to update course collection
    def add_assignment(self, course_id, updated_data):
        self.course_collection.update_one({'course_id': course_id}, {'$set': updated_data})

    def close_DB(self):
        self.client.close()


if __name__ == '__main__':
    course_data = [
        {'course_id' : 'COMS6111',
        'course_name': 'Advanced Database Systems',
        'assignment_list': ['COMS6111_A1', 'COMS6111_A2','COMS6111_A3'],
        'grader_id': 'ac1007'
        },
            {'course_id' : 'ELEN6770',
        'course_name': 'Next Generation Networking',
        'assignment_list': ['ELEN6770_A1', 'ELEN6770_A2', 'ELEN6770_A3'],
        'grader_id': 'ac1007'
        },
        {'course_id' : 'COMS4111',
        'course_name': 'Introduction to Database Systems',
        'assignment_list': ['COMS4111_A1', 'COMS4111_A2', 'COMS4111_A3'],
        'grader_id': 'lu5200'
        },
        {'course_id' : 'COMS1234',
        'course_name': 'Software Development',
        'assignment_list': ['COMS1234_A1'],
        'grader_id': 'xz1332'
        },
        {'course_id' : 'ELEN5567',
        'course_name': 'Content Distribution Networks',
        'assignment_list': ['ELEN5567_A1'],
        'grader_id': 'lu5200'
        },
        {'course_id' : 'ELEN4377',
        'course_name': 'Introduction to Computer Networks',
        'assignment_list': ['ELEN4377_A1'],
        'grader_id':'ac1007'
        },
        {'course_id' : 'COMS4396',
        'course_name': 'Introduction to System Design',
        'assignment_list': ['COMS4396_A1'],
        'grader_id': 'xz1332'
        }
    ]
    course = Course()
    course.insert_many_courses(course_data)
    course.close_DB()
