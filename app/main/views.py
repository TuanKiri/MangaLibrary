from . import main
from ..form import SearchForm
from flask import render_template, request, current_app
from .. import db
from ..models import User, Manga, News, logs, Comment, Tag, manga_tag, Chapter
from datetime import datetime, timedelta

@main.route('/')
def index():
    search_form = SearchForm()

    manga = Manga.query.order_by(Manga.timestamp.desc())

    popular_manga = db.session.query(Manga, db.func.count(logs.c.user_id).label('popular')) \
                                .join(logs) \
                                .group_by(Manga) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5)
    popular_users = db.session.query(User, db.func.count(Comment.user_id).label('popular')) \
                                .join(Comment) \
                                .group_by(User) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5)
    popular_tags = db.session.query(Tag, db.func.count(manga_tag.c.tag_id).label('popular')) \
                                .join(manga_tag) \
                                .group_by(Tag) \
                                .order_by(db.text('popular DESC')) \
                                .limit(15)
    # new_chapter = db.session.query(Manga, Chapter, db.func.max(Chapter.timestamp).label('timestamp')) \
    #                             .join(Chapter) \
    #                             .group_by(Manga) \
    #                             .order_by(db.text('timestamp DESC')) \
    #                             .limit(10)
    new_chapter = []
    news = News.query.order_by(News.timestamp.desc()).limit(5)

    manga_discussion = db.session.query(Manga.id, Manga.title, db.literal('manga').label('type'), db.func.count().label('popular')) \
                                .join(Comment) \
                                .group_by(Comment.manga_id).filter(Comment.timestamp >= datetime.now() - timedelta(days=1))
    news_discussion = db.session.query(News.id, News.title, db.literal('news').label('type'), db.func.count().label('popular')) \
                                .join(Comment) \
                                .group_by(Comment.news_id).filter(Comment.timestamp >= datetime.now() - timedelta(days=1))

    # popular_discussion = news_discussion.union(manga_discussion).order_by(db.text('popular DESC')).limit(5)
    popular_discussion = []
    page = request.args.get('page', 1, type=int)
    pagination = manga.paginate(
    page, per_page=current_app.config['MANGA_LIST_PER_PAGE'],
    error_out=False)
    return render_template('index.html', search_form=search_form, popular_manga=popular_manga, popular_users=popular_users, \
                            news=news, popular_tags=popular_tags, new_chapter=new_chapter, popular_discussion=popular_discussion, pagination=pagination, title="Главная")


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
        search_form.search.data = search_word
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
        search_form.search.data = search_word
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