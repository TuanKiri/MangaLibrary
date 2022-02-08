from ..comment.forms import CommentForm
from datetime import datetime
from .forms import AddMangaForm, EditMangaForm, AddChapterForm
from . import manga
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required, current_user
from .. import db, manga_upload
from ..models import Manga, Permission, Images, Chapter, Comment, Tag
from ..decorators import permission_required

@manga.route('/<int:id>')
def index(id):
    comment_form = CommentForm()
    manga = Manga.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = manga.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANGA_COMMENTS_PER_PAGE'],
        error_out=False)
    return render_template("manga.html", comment_form=comment_form, manga=manga, pagination=pagination, title=manga.title)

@manga.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def add():
    add_manga_form = AddMangaForm()
    if add_manga_form.validate_on_submit():
        manga = Manga(
            title=add_manga_form.title.data,
            author=add_manga_form.author.data,
            tags_string=add_manga_form.tags.data,
            catalog=add_manga_form.catalog.data,
            user=current_user._get_current_object()
        )
        if add_manga_form.image.data:
            forder = str(manga.id)
            manga.image = manga_upload.save(add_manga_form.image.data, folder=forder)
        db.session.add(manga)
        db.session.commit()
        flash('Манга %s добавлена.'% manga.title, 'success')
        return redirect(url_for('.index', id=manga.id))
    return render_template("add_manga.html", edit_manga_form=add_manga_form, title="Добавить мангу")


@manga.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def edit(id):
    manga = Manga.query.get_or_404(id)
    edit_manga_form = EditMangaForm(manga=manga)
    if edit_manga_form.validate_on_submit():
        manga.title=edit_manga_form.title.data
        manga.author=edit_manga_form.author.data
        manga.tags_string=edit_manga_form.tags.data
        manga.catalog=edit_manga_form.catalog.data
        manga.user=current_user._get_current_object()
        manga.timestamp = datetime.utcnow()
        if edit_manga_form.image.data:
            forder = str(manga.id)
            manga.image = manga_upload.save(edit_manga_form.image.data, folder=forder)
        db.session.add(manga)
        db.session.commit()
        flash('Манга %s обновлена.'% manga.title, 'success')
        return redirect(url_for('.index', id=manga.id))
    edit_manga_form.title.data = manga.title
    edit_manga_form.author.data = manga.author
    edit_manga_form.tags.data = manga.tags_string
    edit_manga_form.catalog.data = manga.catalog
    return render_template("add_manga.html", edit_manga_form=edit_manga_form, manga=manga, title=manga.title)


@manga.route('/read/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    manga = Manga.query.get_or_404(id)
    if current_user.is_reading(manga):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', id=manga.id))
    current_user.read(manga)
    db.session.commit()
    return redirect(url_for('.index', id=manga.id))


@manga.route('/unread/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    manga = Manga.query.get_or_404(id)
    if not current_user.is_reading(manga):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', id=manga.id))
    current_user.unread(manga)
    db.session.commit()
    return redirect(url_for('.index', id=manga.id))


@manga.route('/add_chapter/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def add_chapter(id):
    manga = Manga.query.get_or_404(id)
    add_chapter_form = AddChapterForm()
    if add_chapter_form.validate_on_submit():
        chapter = Chapter(
            volume=add_chapter_form.volume.data,
            chapter=add_chapter_form.chapter.data,
            title=add_chapter_form.title.data,
            user=current_user._get_current_object(),
            manga=manga
        )
        for file in request.files.getlist("image"):
            if file.filename:
                forder = str(manga.id) + "/" + str(add_chapter_form.volume.data) + "/" + str(add_chapter_form.chapter.data)
                image = Images(
                    url = manga_upload.save(file, folder=forder),
                    chapter=chapter
                )
                db.session.add(image)
        db.session.add(chapter)
        db.session.commit()
        flash('Глава опубликована.', 'success')
        return redirect(url_for('.index', id=manga.id))
    return render_template("add_chapter.html", edit_chapter_form=add_chapter_form, manga=manga, title=manga.title)


@manga.route('/delete_chapter/<int:id>/<int:volume>/<int:chapter>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.PUBLICATION)
def delete_chapter(id, volume, chapter):
    manga = Manga.query.get_or_404(id)

    current_chapter = manga.chapter.filter_by(
        volume=volume,
        chapter=chapter
    ).first_or_404()

    db.session.delete(current_chapter)
    db.session.commit()
    flash('Глава удалена.', 'success')

    return redirect(url_for('.index', id=manga.id))


@manga.route('<int:id>/<int:volume>/<int:chapter>')
def chapter(id, volume, chapter):
    manga = Manga.query.get_or_404(id)
    
    current_chapter = manga.chapter.filter_by(
        volume=volume,
        chapter=chapter
    ).first_or_404()
    
    pagination_images = current_chapter.image.paginate(
        page=request.args.get('page', 0, type=int), 
        per_page=1, 
        error_out=False
    )

    chapters = manga.chapter.all()
    pagination_chapters = manga.chapter.paginate(
        page=chapters.index(current_chapter) + 1,  
        per_page=1,
        error_out=False
    )
    
    title = f"Том {current_chapter.volume} Глава {current_chapter.chapter}"

    return render_template("chapter.html", pagination_chapters=pagination_chapters, current_chapter=current_chapter, chapters=chapters, \
                            pagination_images=pagination_images, manga=manga, title=title)


@manga.route('/tag/<int:id>')
def tag(id):
    tag = Tag.query.get_or_404(id)
    manga =  Manga.query.filter(Manga.tags.any(Tag.id == tag.id)) \
                        .group_by(Manga.id) \
                        .order_by(Manga.timestamp.desc())

    page = request.args.get('page', 1, type=int)
    pagination = manga.paginate(
    page, per_page=current_app.config['MANGA_LIST_PER_PAGE'], 
    error_out=False)
    return render_template('tag.html', pagination=pagination, tag=tag)