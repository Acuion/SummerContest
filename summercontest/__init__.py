from postgres import Postgres
from summercontest import privatedata
from flask import Flask

def pgInstance():
    return Postgres(privatedata.pgconnectionstring)

app = Flask(__name__)

from summercontest import cache
from summercontest import groupsProvider
from summercontest import frontend
