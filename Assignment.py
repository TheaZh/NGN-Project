from pymongo import MongoClient

class Assignment:
    def __init__(self):
        self.mongo_uri = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['assignment-management-system']
        self.assignment_collection = self.db['Assignment']

    def insert_assignments(self, seed_data):
        self.assignment_collection.insert_many(seed_data)

    def close_DB(self):
        self.client.close()

if __name__ == '__main__':
    '''assignment_data = [
        {'assignment_id': 'COMS6111_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS6111_A2',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS6111_A3',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A2',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN6770_A3',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A2',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4111_A3',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS1234_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN5567_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'ELEN4377_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        },
        {'assignment_id': 'COMS4396_A1',
        'submitted_file_dict': {},
        'upload_file_dict':{},
        'grade_dict': {}
        }
    ]
    assig = Assignment()
    assig.insert_assignments(assignment_data)
    assig.close_DB()'''
