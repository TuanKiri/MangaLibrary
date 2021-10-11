from flask import render_template
from . import news
from .forms import NewsForm
from ..comment.forms import CommentForm
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required, current_user
from .. import db, news_upload
from ..models import News, Images, Comment
from ..decorators import admin_required


@news.route('/<title>')
def index(title):
    comment_form = CommentForm()
    news= News.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = news.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANGA_COMMENTS_PER_PAGE'],
        error_out=False)
    return render_template('news.html', comment_form=comment_form, news=news, pagination=pagination, title=news.title)


@news.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    news_form = NewsForm()
    if news_form.validate_on_submit():
        news = News(
            title=news_form.title.data,
            body=news_form.news.data,
            user=current_user._get_current_object()
        )
        for file in request.files.getlist("image"):
            if file.filename:
                forder = str(news_form.title.data)
                image = Images(
                    image = news_upload.save(file, folder=forder),
                    news=news
                )
                db.session.add(image)
        db.session.add(news)
        db.session.commit()
        flash('Новость опубликована.', 'success')
        return redirect(url_for('.index', title=news.title))
    return render_template('add_news.html', news_form=news_form, title=u"Создать новость")