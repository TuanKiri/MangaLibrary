from . import main
from ..form import SearchForm
from flask import render_template, request, current_app
from .. import db
from ..models import User, Manga, News, logs, Comment, Tag


@main.route('/')
def index():
    search_form = SearchForm()
    theme = bool(request.cookies.get('theme', ''))
    manga = Manga.query.order_by(Manga.timestamp.desc())

    popular_manga = db.session.query(Manga, db.func.count(logs.c.user_id).label('popular')) \
                                .join(logs).group_by(Manga) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5)
    popular_users = db.session.query(User, db.func.count(Comment.user_id).label('popular')) \
                                .join(Comment).group_by(User) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5)

    news = News.query.order_by(News.timestamp.desc()).limit(5)
    page = request.args.get('page', 1, type=int)
    pagination = manga.paginate(
    page, per_page=current_app.config['NEWS_LIST_PER_PAGE'],
    error_out=False)
    return render_template('index.html', search_form=search_form, theme=theme, popular_manga=popular_manga, popular_users=popular_users, \
                            news=news, pagination=pagination, title="Главная")


@main.route('/manga-list', methods=['GET'])
def manga_list():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    manga = Manga.query
    if search_word:
        manga = manga.filter(Manga.title.ilike('%' + search_word + '%'))
        search_form.search.data = search_word
    else:
        manga = manga.order_by(Manga.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = manga.paginate(
    page, per_page=current_app.config['MANGA_LIST_PER_PAGE'],
    error_out=False)
    return render_template('manga_list.html', search_form=search_form, pagination=pagination, title="Манга")

@main.route('/tags-list', methods=['GET'])
def tags_list():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    tags = Tag.query
    if search_word:
        tags = tags.filter(Tag.name.ilike('%' + search_word + '%'))
    page = request.args.get('page', 1, type=int)
    pagination = tags.paginate(
    page, per_page=current_app.config['TAGS_LIST_PER_PAGE'],
    error_out=False)
    return render_template('tags_list.html', pagination=pagination, search_form=search_form, title="Теги")

@main.route('/users-list', methods=['GET'])
def users_list():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    users = User.query
    if search_word:
        users = users.filter(User.username.ilike('%' + search_word + '%'))
    page = request.args.get('page', 1, type=int)
    pagination = users.paginate(
    page, per_page=current_app.config['USER_LIST_PER_PAGE'],
    error_out=False)
    return render_template('users_list.html', search_form=search_form, pagination=pagination, title="Пользователи")

@main.route('/news-list')
def news_list():
    news = News.query.order_by(News.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = news.paginate(
    page, per_page=current_app.config['NEWS_LIST_PER_PAGE'],
    error_out=False)
    return render_template('news_list.html', pagination=pagination, title="Новости")