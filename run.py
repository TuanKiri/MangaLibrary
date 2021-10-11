import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import Role, follows, logs, User, Manga, Chapter, manga_tag, Tag, Comment, News, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Role=Role, follows=follows, logs=logs, User=User, 
                Manga=Manga, Chapter=Chapter, manga_tag=manga_tag, Tag=Tag, 
                Comment=Comment, News=News, Permission=Permission)