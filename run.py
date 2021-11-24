import os
import click
import sys
from flask_migrate import Migrate
from app import create_app, db, celery
from app.models import Role, follows, logs, User, Manga, Chapter, manga_tag, Tag, Comment, News, Permission

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'development', celery=celery)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Role=Role, follows=follows, logs=logs, User=User, 
                Manga=Manga, Chapter=Chapter, manga_tag=manga_tag, Tag=Tag, 
                Comment=Comment, News=News, Permission=Permission)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
                help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    print('\n\nUnittest:\n')
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        print('\n\nCoverage Summary:\n')
        COV.report()
        COV.erase()