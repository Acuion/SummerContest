from postgres import Postgres
from summercontest import privatedata
from flask import Flask

PGI = Postgres(privatedata.pgconnectionstring)

def pgInstance():
    return PGI

app = Flask(__name__)

from summercontest import cache
from summercontest import groupsProvider
from summercontest import frontend
