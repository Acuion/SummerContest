import json
import time
from flask import request
from summercontest import app
from summercontest import scoreGetter
from summercontest import groupsProvider
from summercontest import pgInstance

@app.route("/solvedCached")
def scoreApi():
    participantId = request.args.get('id')
    if not participantId:
        return 'oops'
    cachedScores = pgInstance().one('SELECT * FROM suco WHERE id=%(id)s', {'id': participantId}, back_as=dict)
    return json.dumps(cachedScores)

def buildCache():
    startTime = time.time()
    groups = json.loads(groupsProvider.groupApi())
    print('loading data')
    groups = scoreGetter.getSolved(groups)
    for participant in groups:
        print('caching', participant['id'])
        curr = pgInstance().one('SELECT * FROM suco WHERE id=%(id)s', {'id': participant['id']}, back_as=dict)
        if curr:
            # exists
            lastchange = curr['lastchange']
            if curr['acmp'] < participant['acmp'] or curr['timus'] < participant['timus']:
                lastchange = int(time.time())
                print('changed', lastchange)
            pgInstance().run("UPDATE suco SET acmp=%(acmp)s, timus=%(timus)s, lastchange=%(lastchange)s, power=%(power)s, power_hint=%(power_hint)s WHERE id=%(id)s",
            {'id': participant['id'], 'acmp': participant['acmp'], 'timus': participant['timus'],
            'lastchange': lastchange, 'power': participant['power'], 'power_hint': participant['power_hint']})
        else:
            # new
            pgInstance().run("INSERT INTO suco values(%(id)s, %(acmp)s, %(timus)s, -1, %(power)s, %(power_hint)s)",
            {'id': participant['id'], 'acmp': participant['acmp'], 'timus': participant['timus'],
            'power': participant['power'], 'power_hint': participant['power_hint']})
    print('exec time = ', time.time() - startTime, 'sec')
