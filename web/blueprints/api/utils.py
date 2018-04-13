import json


def response(status, message):
    data = {
        'status': status,
    }

    if isinstance(message, dict):
        data['message'] = message
    else:
        data['message'] = "'"+message+"'"

    return json.dumps(data)
