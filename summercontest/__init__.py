from postgres import Postgres
from summercontest import privatedata
from flask import Flask

PGI = None

def pgInstance():
    global PGI
    if PGI is None:
        PGI = Postgres(privatedata.pgconnectionstring)
    return PGI

app = Flask(__name__)

from summercontest import cache
from summercontest import groupsProvider
from summercontest import frontend

from werkzeug.debug import DebuggedApplication
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
