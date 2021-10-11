from ..comment.forms import CommentForm
from .forms import EditMangaForm, EditChapterForm
from . import manga
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required, current_user
from .. import db, manga_upload
from ..models import Manga, Permission, Images, Chapter, Comment, Tag
from ..decorators import permission_required

@manga.route('/<title>')
def index(title):
    comment_form = CommentForm()
    manga = Manga.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = manga.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANGA_COMMENTS_PER_PAGE'],
        error_out=False)
    return render_template("manga.html", comment_form=comment_form, manga=manga, pagination=pagination, title=manga.title)

@manga.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def add():
    edit_manga_form = EditMangaForm()
    if edit_manga_form.validate_on_submit():
        manga = Manga(
            title=edit_manga_form.title.data,
            author=edit_manga_form.author.data,
            tags_string=edit_manga_form.tags.data,
            catalog=edit_manga_form.catalog.data,
            user=current_user._get_current_object()
        )
        if edit_manga_form.image.data:
            print(type(edit_manga_form.image.data))
            forder = str(edit_manga_form.title.data)
            manga.image = manga_upload.save(edit_manga_form.image.data, folder=forder)
        db.session.add(manga)
        db.session.commit()
        flash('Манга %s добавлена.'% manga.title, 'success')
        return redirect(url_for('.index', title=manga.title))
    return render_template("add_manga.html", edit_manga_form=edit_manga_form, title="Добавить мангу")


@manga.route('/edit/<title>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def edit(title):
    manga = Manga.query.filter_by(title=title).first_or_404()
    edit_manga_form = EditMangaForm()
    if edit_manga_form.validate_on_submit():
        manga.title=edit_manga_form.title.data
        manga.author=edit_manga_form.author.data
        manga.tags_string=edit_manga_form.tags.data
        manga.catalog=edit_manga_form.catalog.data
        manga.user=current_user._get_current_object()
        if edit_manga_form.image.data:
            forder = str(edit_manga_form.title.data)
            manga.image = manga_upload.save(edit_manga_form.image.data, folder=forder)
        db.session.add(manga)
        db.session.commit()
        flash('Манга %s обновлена.'% manga.title, 'success')
        return redirect(url_for('.index', title=manga.title))
    edit_manga_form.title.data = manga.title
    edit_manga_form.author.data = manga.author
    edit_manga_form.tags.data = manga.tags_string
    edit_manga_form.catalog.data = manga.catalog
    return render_template("add_manga.html", edit_manga_form=edit_manga_form, manga=manga, title=manga.title)


@manga.route('/read/<title>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(title):
    manga = Manga.query.filter_by(title=title).first_or_404()
    if manga is None:
        flash('Такой манги нет.', 'alert')
        return redirect(url_for('main.index'))
    if current_user.is_reading(manga):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', title=manga.title))
    current_user.read(manga)
    db.session.commit()
    flash('Вы теперь подписаны на %s.' % manga.title, 'success')
    return redirect(url_for('.index', title=manga.title))


@manga.route('/unread/<title>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(title):
    manga = Manga.query.filter_by(title=title).first_or_404()
    if manga is None:
        flash('Такой манги нет.', 'alert')
        return redirect(url_for('main.index'))
    if not current_user.is_reading(manga):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', title=manga.title))
    current_user.unread(manga)
    db.session.commit()
    flash('Вы больше не подписаны на %s.' % manga.title, 'success')
    return redirect(url_for('.index', title=manga.title))


@manga.route('/add_chapter/<title>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def add_chapter(title):
    manga = Manga.query.filter_by(title=title).first_or_404()
    edit_chapter_form = EditChapterForm()
    if edit_chapter_form.validate_on_submit():
        chapter = Chapter(
            volume=edit_chapter_form.volume.data,
            chapter=edit_chapter_form.chapter.data,
            title=edit_chapter_form.title.data,
            user=current_user._get_current_object(),
            manga=manga
        )
        for file in request.files.getlist("image"):
            if file.filename:
                forder = manga.title + "/" + str(edit_chapter_form.volume.data) + "/" + str(edit_chapter_form.chapter.data)
                image = Images(
                    image = manga_upload.save(file, folder=forder),
                    chapter=chapter
                )
                db.session.add(image)
        db.session.add(chapter)
        db.session.commit()
        flash('Глава опубликована.', 'success')
        return redirect(url_for('.index', title=manga.title))
    return render_template("add_chapter.html", edit_chapter_form=edit_chapter_form)

@manga.route('<title>/<volume>/<chapter>')
def chapter(title, volume, chapter):
    manga = Manga.query.filter_by(title=title).first_or_404()
    
    current_chapter = manga.chapter.filter_by(
            volume=volume,
            chapter=chapter
        ).first_or_404()

    chapters = manga.chapter.all()
    page = chapters.index(current_chapter) + 1
    pagination = manga.chapter.paginate(
        page,  per_page=1,
        error_out=False)
        
    return render_template("chapter.html", pagination=pagination, manga=manga, title="Том " + current_chapter.volume + " Глава " + current_chapter.chapter)

@manga.route('/tag/<name>')
def tag(name):
    manga =  Manga.query.filter(Manga.tags.any(Tag.name.ilike(name))) \
                        .group_by(Manga.id) \
                        .order_by(Manga.timestamp.desc())

    page = request.args.get('page', 1, type=int)
    pagination = manga.paginate(
    page, per_page=3, error_out=False)
    return render_template('tag.html', pagination=pagination, name=name)