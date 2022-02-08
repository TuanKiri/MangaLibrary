from . import main
from ..form import SearchForm
from flask import render_template, request, current_app
from .. import db
from ..models import User, Manga, News, logs, Comment, Tag, manga_tag, Chapter

@main.route('/')
def index():
    search_form = SearchForm()
    
    new_manga = Manga.query.order_by(Manga.timestamp.desc())

    popular_manga = db.session.query(Manga, db.func.count(logs.c.user_id).label('popular')) \
                                .join(logs) \
                                .group_by(Manga) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5).from_self(Manga)
    popular_users = db.session.query(User, db.func.count(Comment.user_id).label('popular')) \
                                .join(Comment) \
                                .group_by(User) \
                                .order_by(db.text('popular DESC')) \
                                .limit(5).from_self(User)
    popular_tags = db.session.query(Tag, db.func.count(manga_tag.c.tag_id).label('popular')) \
                                .join(manga_tag) \
                                .group_by(Tag) \
                                .order_by(db.text('popular DESC')) \
                                .limit(48).from_self(Tag)
    new_chapters = db.session.query(Manga, Chapter, db.func.max(Chapter.timestamp).label('timestamp')) \
                                .join(Chapter) \
                                .group_by(Manga.id, Chapter.id) \
                                .order_by(db.text('timestamp DESC')).limit(8).from_self(Manga, Chapter)

    last_news = News.query.order_by(News.timestamp.desc()).limit(6)
    
    page = request.args.get('page', 1, type=int)
    pagination_new_manga = new_manga.paginate(
    page, per_page=current_app.config['MANGA_LIST_PER_PAGE'],
    error_out=False)
    return render_template('index.html', search_form=search_form, popular_manga=popular_manga, popular_users=popular_users, \
                            last_news=last_news, popular_tags=popular_tags, new_chapters=new_chapters, pagination_new_manga=pagination_new_manga, title="Главная")


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