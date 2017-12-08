from pymongo import MongoClient

'''
#### Default Schema ####

new_user = {
    'uni': uni,
    'name': name,
    'email': email,
    'password': password,
    'isGrader': True/False,
    'course_list': []
    }

'''
class User:
    def __init__(self):
        # MongoDB URI - for normal collections
        self.mongo_uri = "mongodb://assignment:assignment123@ds161873.mlab.com:61873/assignment-management-system"
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['assignment-management-system']
        self.user_collection = self.db['User']

    def insert_user(self, uni, name, email, password, isGrader, course_list):
        seed_data = {'uni': uni,
                    'name': name,
                    'email': email,
                    'password': password,
                    'isGrader': isGrader,
                    'course_list': course_list
                    }
        id = self.user_collection.insert(seed_data)
        print id

    def insert_many_users(self, seed_data):
        ids = self.user_collection.insert_many(seed_data)
        print ids

    def close_DB(self):
        self.client.close()


if __name__ == '__main__':
    '''student_data = [
                {'uni': 'ab0001',
                'name': 'Avil',
                'email': 'ab0001@gmail.com',
                'password': 'ab0001',
                'isGrader': False,
                'course_list': ['ELEN6770', 'COMS4111', 'ELEN5567','ELEN4377']
                },
                {'uni': 'ab0002',
                'name': 'Anna',
                'email': 'ab0002@gmail.com',
                'password': 'ab0002',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234', 'ELEN5567']
                },
                {'uni': 'ab0005',
                'name': 'Abbie',
                'email': 'ab0005@gmail.com',
                'password': 'ab0005',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234']
                },
                {'uni': 'ce1022',
                'name': 'Cady',
                'email': 'ce1022@gmail.com',
                'password': 'ce1022',
                'isGrader': False,
                'course_list': ['ELEN5567','ELEN4377']
                },
                {'uni': 'ap1050',
                'name': 'Alex',
                'email': 'ap1050@gmail.com',
                'password': 'ap1050',
                'isGrader': False,
                'course_list': ['COMS4396', 'COMS4111', 'ELEN4377']
                },
                {'uni': 'uz0202',
                'name': 'Ura',
                'email': 'uz0202@gmail.com',
                'password': 'uz0202',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234','COMS4396']
                },
                {'uni': 'fc2345',
                'name': 'Fay',
                'email': 'fc2345@gmail.com',
                'password': 'fc2345',
                'isGrader': False,
                'course_list': ['COMS4111', 'ELEN4377', 'ELEN5567']
                },
                {'uni': 'zh1266',
                'name': 'Zara',
                'email': 'zh1266@gmail.com',
                'password': 'zh1266',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234']
                },
                {'uni': 'pd2222',
                'name': 'Peter',
                'email': 'pd2222@gmail.com',
                'password': 'pd2222',
                'isGrader': False,
                'course_list': ['COMS1234', 'ELEN6770', 'COMS4396']
                },
                {'uni': 'ac1256',
                'name': 'Amy',
                'email': 'ac1256@gmail.com',
                'password': 'ac1256',
                'isGrader': False,
                'course_list': ['ELEN5567','ELEN4377', 'COMS4396']
                },
                {'uni': 'fg8745',
                'name': 'Felix',
                'email': 'fg8745@gmail.com',
                'password': 'fg8745',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234','ELEN5567','ELEN4377']
                },
                {'uni': 'jk0033',
                'name': 'Jackson',
                'email': 'jk0033@gmail.com',
                'password': 'jk0033',
                'isGrader': False,
                'course_list': ['COMS4396','ELEN5567']
                },
                {'uni': 'mp1555',
                'name': 'May',
                'email': 'mp1555@gmail.com',
                'password': 'mp1555',
                'isGrader': False,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS1234','COMS4396']
                }
    ]

    grader_data = [
                {'uni': 'ac1007',
                'name': 'Alex',
                'email': 'ac1007@gmail.com',
                'password': 'ac1007',
                'isGrader': True,
                'course_list': ['COMS6111', 'ELEN6770', 'COMS4111']
                },
                {'uni': 'lu5200',
                'name': 'Lisa',
                'email': 'lu5200@gmail.com',
                'password': 'lu5200',
                'isGrader': True,
                'course_list': ['ELEN5567', 'ELEN4377']
                },
                {'uni': 'xz1332',
                'name': 'Xavier',
                'email': 'xz1332@gmail.com',
                'password': 'xz1332',
                'isGrader': True,
                'course_list': ['COMS4396','COMS1234']
                }
    ]
    print student_data
    user = User()
    user.insert_many_users(student_data)
    user.insert_many_users(grader_data)
    user.close_DB()'''
