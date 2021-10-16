
from flask import render_template
from . import errors


@errors.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@errors.app_errorhandler(429)
def internal_server_error(e):
    return render_template('429.html'), 429