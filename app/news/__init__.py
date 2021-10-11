from flask import Blueprint

news = Blueprint('news', __name__, url_prefix='/news', template_folder='../news/templates')

from . import views