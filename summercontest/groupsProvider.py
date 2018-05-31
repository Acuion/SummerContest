from summercontest import app
from flask import request

@app.route("/group")
def groupApi():
    groupId = request.args.get('id')
    if not groupId or not groupId.isdigit():
        return 'Not enough arguments'
    with open('/var/suco/group{}.json'.format(groupId), 'r') as f:
        return f.read()
