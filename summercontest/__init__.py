from flask import Flask

app = Flask(__name__)

from summercontest import scoreGetter
from summercontest import groupsProvider
