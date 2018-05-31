from summercontest import app
from flask import render_template

@app.route('/summer')
def frontend():
    return render_template('index.html')
