from flask import Blueprint

comment = Blueprint('comment', __name__, url_prefix='/comments', template_folder='templates')

from . import views
