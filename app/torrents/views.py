from . import torrents
from flask_login import login_required
from flask import render_template
from ..form import SearchForm

@torrents.route('/')
@login_required
def index():
    search_form = SearchForm()
    return render_template('torrents.html', search_form=search_form, title="torrents")