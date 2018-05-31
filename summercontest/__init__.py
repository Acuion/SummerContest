from flask import Flask

app = Flask(__name__)

from summercontest import cache
from summercontest import groupsProvider
from summercontest import frontend
