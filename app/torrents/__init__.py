from flask import Blueprint

torrents = Blueprint('torrents', __name__, url_prefix='/torrents', template_folder='../torrents/templates')

from . import views