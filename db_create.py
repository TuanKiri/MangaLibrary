import os
from app import create_app, db
from app.models import Role, Tag

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()
Tag.insert_tags()
db.session.commit()
app_ctx.pop()