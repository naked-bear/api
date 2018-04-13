from pymongo import MongoClient
from bson.objectid import ObjectId
import web.config as config
import json


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
                    return self.response(True, user)
                else:
                    return self.response(False, 'Your account is suspended, please contact support@nakedbear.io.')
            else:
                return self.response(False, 'A confirmation email has been sent to '+user['email']+'. Please verify before signing in.')
        else:
            return self.response(False, 'Username or Password Incorrect')

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

                return self.response(True, 'Account created successfully. A confirmation email has been sent to '+email+'.')

            else:
                if user['email'] == email:
                    return self.response(False, 'An account with this email already exists')
                elif user['username'] == username:
                    return self.response(False, 'An account with this username already exists')
        else:
            return self.response(False, 'Please fill all fields')

    def forgot(self, email):
        return

    def is_valid(self, inputs):
        for i in inputs:
            if len(i) == 0:
                return False
        return True

    def response(self, status, message):
        data = {
            'status': status
        }
        if isinstance(message, dict):
            data['message'] = message
        else:
            data['message'] = "'"+message+"'"
        
        return json.dumps(data)

