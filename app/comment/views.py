from .forms import CommentForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Manga, News, Comment, Permission
from ..decorators import permission_required
from . import comment


@comment.route('/add_manga_comment/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.COMMENT)
def add_manga_comment(id):
    comment_form = CommentForm()
    manga = Manga.query.get_or_404(id)
    if comment_form.comment.data:
        comment = Comment(
            user=current_user._get_current_object(), 
            manga=manga, 
            body=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
    return redirect(url_for('manga.index', id=manga.id))

@comment.route('/add_news_comment/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.COMMENT)
def add_news_comment(id):
    comment_form = CommentForm()
    news = News.query.get_or_404(id)
    if comment_form.comment.data:
        comment = Comment(
            user=current_user._get_current_object(), 
            news=news, 
            body=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
    return redirect(url_for('news.index', id=news.id))

@comment.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=15,
        error_out=False)
    return render_template('moderation_comments.html',
                           pagination=pagination, page=page, title="Модерация")


@comment.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@comment.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))



