from flask import Blueprint, request
import json
from Users import Users

api = Blueprint('api',  __name__)


@api.route('/api/init', methods=['POST'])
def init():
    # register client; save to database
    # send open connection request
    # respond with connection url
    return


@api.route('/api/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        return Users().authenticate(data['username'], data['password'])


@api.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True, force=True)
    return Users().signup(data['fullName'], data['username'], data['email'], data['password'])


@api.route('/api/auth/forgot', methods=['POST'])
def forgot():
    data = request.get_json(silent=True, force=True)
    return Users().authenticate(data['email'])


@api.route('/download/<username>/<filename>')
def download(username, filename):
    # check if file exists for that user
    # check if connection exits
    # request file from connection
    # return file stream
    return