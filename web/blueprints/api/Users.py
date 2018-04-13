from pymongo import MongoClient
from bson.objectid import ObjectId
import config as config
import utils


class Users:

    def __init__(self):
        self.client = MongoClient(config.mongodb['host'], config.mongodb['port'])

    def authenticate(self, username, password):

        user = self.client[config.mongodb['database']]['users'].find_one({
            'username': username,
            'password': password
        })

        if user is not None:
            if user['isConfirmed']:
                if user['isSuspended'] is not True:
                    return utils.response(True, user)
                else:
                    return utils.response(False, 'Your account is suspended, please contact support@nakedbear.io.')
            else:
                return utils.response(False, 'A confirmation email has been sent to '+user['email']+'. Please verify before signing in.')
        else:
            return utils.response(False, 'Username or Password Incorrect')

    def signup(self, full_name, username, email, password):

        if self.is_valid([full_name, username, email, password]):

            user = self.client[config.mongodb['database']]['users'].find_one({
                "$or": [{
                    "username": username
                }, {
                    "email": email
                }]
            })

            if user is None:

                self.client[config.mongodb['database']]['users'].insert_one({
                    'fullName': full_name,
                    'username': username,
                    'email': email,
                    'password': password
                })

                return utils.response(True, 'Account created successfully. A confirmation email has been sent to '+email+'.')

            else:
                if user['email'] == email:
                    return utils.response(False, 'An account with this email already exists')
                elif user['username'] == username:
                    return utils.response(False, 'An account with this username already exists')
        else:
            return utils.response(False, 'Please fill all fields')

    def forgot(self, email):
        return

    def is_valid(self, inputs):
        for i in inputs:
            if len(i) == 0:
                return False
        return True