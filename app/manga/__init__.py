from flask import Blueprint

manga = Blueprint('manga', __name__, url_prefix='/manga', template_folder='templates')

from . import views
