from summercontest import app
from flask import request
import json

@app.route("/groups")
def groupApi():
    with open('/var/suco/groups.txt', 'r', encoding='utf-8') as f:
        rawGroups = f.readlines()
        groups = []
        for line in rawGroups:
            cid,f,i,o,div,cf,timus,acmp = line.split()
            groups.append({'id': cid, 'fio': '{} {} {}'.format(f,i,o), 'div': div, 'cf': cf, 'timus': timus, 'acmp': acmp})
        return json.dumps(groups)
