from . import torrents
from flask_login import login_required
from flask import render_template

@torrents.route('/')
@login_required
def index():
    return render_template('torrents.html', title="torrents")