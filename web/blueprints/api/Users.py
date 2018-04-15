from pymongo import MongoClient
from bson.objectid import ObjectId
from sparkpost import SparkPost
import web.config as config
import json
import base64
import string
import random


class Users:

    def __init__(self):
        self.client = MongoClient(config.mongodb['host'], config.mongodb['port'])

    def authenticate(self, username, password):

        user = self.client[config.mongodb['database']]['users'].find_one({
            'username': username,
            'password': base64.b64encode(password.encode("utf-8"))
        })

        if user is not None:
            if user['isConfirmed']:
                if user['isSuspended'] is not True:
                    del user['password']
                    user['_id'] = str(user['_id'])
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

                confirm = self.generate_random()

                self.client[config.mongodb['database']]['users'].insert_one({
                    'fullName': full_name,
                    'username': username,
                    'email': email,
                    'password': base64.b64encode(password.encode("utf-8")),
                    'isConfirmed': False,
                    'isSuspended': False,
                    'confirm': confirm,
                    'plan': 0
                })

                with open('web/templates/confirmation_email.html', 'r') as html_file:
                    
                    with open('sparkpost.key', 'r') as key_file:
                        html = html_file.read().replace('{{confirm}}', confirm)
                        sp = SparkPost(key_file.read().replace('\n', ''))
                        sp.transmissions.send(
                            recipients=[email],
                            html=html,
                            from_email='do_not_reply@nakedbear.io',
                            subject='Hello from NakedBear'
                        )

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

    def verify(self, confirmation):
        
        if self.is_valid(confirmation):
            self.client[config.mongodb['database']]['users'].update_one({
                "confirm": confirmation
            }, {
                "$set": {
                    "isConfirmed": True
                }
            }, upsert=False)
            return self.response(True, '<center><h1>Email address confirmed!</h1><small>You may close this window</small>')
        else:
            return self.response(False, '<center><h1>Failed to verify email address :(</h1><small>Contact support@nakedbear.io</small></center>')

    def is_valid(self, inputs):
        for i in inputs:
            if len(i) == 0:
                return False
        return True

    def response(self, status, message):
        data = {
            'status': status,
            'message': message
        }
        
        return json.dumps(data)

    def generate_random(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

