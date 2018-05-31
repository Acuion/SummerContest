import json
from flask import request
from summercontest import app
from summercontest import scoreGetter

@app.route("/scoresCached")
def scoreApi():
    acmpId = request.args.get('acmp')
    timusId = request.args.get('timus')
    cfHandle = request.args.get('cf')
    if not acmpId or not timusId or not cfHandle:
        return 'Not enough arguments'
    cachedScores = scoreGetter.getScores(acmpId, timusId, cfHandle) # not cached yet
    return json.dumps(cachedScores)
