from summercontest import app
from flask import request
import json

@app.route("/groups")
def groupApi():
    with open('/var/suco/groups-2019.txt', 'r', encoding='utf-8') as f:
        rawGroups = f.readlines()
        groups = []
        for line in rawGroups:
            cid, f, i, o, div, timus, acmp = line.split()
            if '0' == timus or '0' == acmp:
                continue
            groups.append({'id': cid, 'fio': '{} {}'.format(i,f), 'div': div, 'timus': timus, 'acmp': acmp})
        return json.dumps(groups)
