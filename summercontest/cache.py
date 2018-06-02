import json
from flask import request
from summercontest import app
from summercontest import scoreGetter
from summercontest import groupsProvider
from summercontest import pgInstance

@app.route("/solvedCached")
def scoreApi():
    acmpId = request.args.get('acmp')
    timusId = request.args.get('timus')
    cfHandle = request.args.get('cf')
    if not acmpId or not timusId or not cfHandle:
        return 'Not enough arguments'
    cachedScores = pgInstance().one('SELECT * FROM suco WHERE handle=%(handle)s', {'handle': cfHandle}, back_as=dict)
    return json.dumps(cachedScores)

def buildCache():
    groups = json.loads(groupsProvider.groupApi())
    for participant in groups:
        print('caching', participant['cf'])
        scoresToCache = scoreGetter.getSolved(participant['acmp'], participant['timus'], participant['cf'])
        if pgInstance().one('SELECT COUNT(*) FROM suco WHERE handle=%(handle)s', {'handle': participant['cf']}, back_as=dict) > 0:
            # exists
            pgInstance().run("UPDATE suco SET acmp=%(acmp)s, timus=%(timus)s, cfdiv1=%(cfdiv1)s, cfdiv23=%(cfdiv23)s WHERE handle=%(handle)s",
            {'handle': participant['cf'], 'acmp': scoresToCache['acmp'], 'cfdiv1': scoresToCache['cfdiv1'], 'cfdiv23': scoresToCache['cfdiv23'], 'timus': scoresToCache['timus']})
        else:
            # new
            pgInstance().run("INSERT INTO suco values(%(handle)s, %(acmp)s, %(timus)s, %(cfdiv1)s, %(cfdiv23)s)",
            {'handle': participant['cf'], 'acmp': scoresToCache['acmp'], 'cfdiv1': scoresToCache['cfdiv1'], 'cfdiv23': scoresToCache['cfdiv23'], 'timus': scoresToCache['timus']})
