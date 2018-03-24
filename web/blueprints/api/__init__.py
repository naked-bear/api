from flask import Flask, Blueprint

api = Blueprint('api',  __name__)

@api.route('/api/init', methods=['POST'])
def init():
    # register client; save to database
    # send open connection request
    # respond with connection url
    return


@api.route('/download/<username>/<filename>')
def download(username, filename):
    # check if file exists for that user
    # check if connection exits
    # request file from connection
    # return file stream
    return