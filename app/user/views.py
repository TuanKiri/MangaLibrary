from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import user
from .forms import EditProfileForm, EditProfileAdminForm, BanForm
from .. import db, users_upload
from ..models import Comment, User, Role, Permission, Manga, follows, Ban
from ..decorators import admin_required, permission_required

@user.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    mode = request.args.get('show', 1, type=int)

    show = {
        1: user.manga.order_by(Manga.timestamp.desc()),
        2: user.manga_user.order_by(Manga.timestamp.desc()),
        3: user.comments.order_by(Comment.timestamp.desc()),
        4: user.followed.order_by(follows.c.timestamp.desc())
    } 

    if mode in show:
        query = show[mode]

        pagination = query.paginate(
            page, per_page=current_app.config['USER_FOLLOWERS_PER_PAGE'],
            error_out=False)
        return render_template("user.html", user=user, title=user.username, pagination=pagination, mode=mode)
    return render_template("user.html", user=user, title=user.username)

@user.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit(username):
    edit_profile_form = EditProfileForm()
    if edit_profile_form.validate_on_submit():
        if edit_profile_form.avatar.data:
            forder = str(current_user.username) + "/avatar"
            avatar_name = users_upload.save(edit_profile_form.avatar.data, folder=forder)
            current_user.avatar = avatar_name
        if edit_profile_form.background.data:
            forder = str(current_user.username) + "/background"
            current_user.background = users_upload.save(edit_profile_form.background.data, folder=forder)
        current_user.location = edit_profile_form.location.data
        current_user.name = edit_profile_form.name.data
        current_user.site = edit_profile_form.site.data
        current_user.about_me = edit_profile_form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Профиль обновлен.', 'info')
        return redirect(url_for('.index', username=current_user.username))
    edit_profile_form.location.data = current_user.location
    edit_profile_form.name.data = current_user.name
    edit_profile_form.site.data = current_user.site
    edit_profile_form.about_me.data = current_user.about_me
    return render_template("user_edit.html", edit_profile_form=edit_profile_form, title=current_user.username)

@user.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(username):
    user = User.query.filter_by(username=username).first_or_404()
    edit_profile_admin_form = EditProfileAdminForm(user=user)
    if edit_profile_admin_form.validate_on_submit():
        if edit_profile_admin_form.avatar.data:
            forder = str(user.username) + "/avatar"
            user.avatar = users_upload.save(edit_profile_admin_form.avatar.data, folder=forder)
        if edit_profile_admin_form.background.data:
            forder = str(user.username) + "/background"
            user.background = users_upload.save(edit_profile_admin_form.background.data, folder=forder)
        user.email = edit_profile_admin_form.email.data
        user.username = edit_profile_admin_form.username.data
        user.confirmed = edit_profile_admin_form.confirmed.data
        if not user.banned:
            user.role = Role.query.get(edit_profile_admin_form.role.data)
        user.location = edit_profile_admin_form.location.data
        user.name = edit_profile_admin_form.name.data
        user.site = edit_profile_admin_form.site.data
        user.about_me = edit_profile_admin_form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Профиль обновлен.', 'info')
        return redirect(url_for('.index', username=user.username))
    edit_profile_admin_form.email.data = user.email
    edit_profile_admin_form.username.data = user.username
    edit_profile_admin_form.confirmed.data = user.confirmed
    edit_profile_admin_form.role.data = user.role_id
    edit_profile_admin_form.location.data = user.location
    edit_profile_admin_form.name.data = user.name
    edit_profile_admin_form.site.data = user.site
    edit_profile_admin_form.about_me.data = user.about_me
    return render_template("user_edit_admin.html", edit_profile_admin_form=edit_profile_admin_form, user=user, title=user.username)


@user.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя нет.', 'alert')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Вы теперь подписаны на %s.' % username, 'success')
    return redirect(url_for('.index', username=username))


@user.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя нет.', 'alert')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('Вы не подписаны на данного пользователя.', 'warning')
        return redirect(url_for('.index', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Вы больше не подписаны на %s.' % username, 'success')
    return redirect(url_for('.index', username=username))


@user.route('/banned/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def banned(username):
    ban_form = BanForm()

    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя нет.', 'alert')
        return redirect(url_for('.index', username=username))
    
    ban = Ban.query.filter_by(id=user.id).first()
    if ban:
        flash('Пользователь в бане.', 'alert')
        return redirect(url_for('.index', username=username))

    if ban_form.validate_on_submit():
        ban = Ban(
            admin_id=current_user.id,
            user_id=user.id,
            reason=ban_form.reason.data,
            last_role=user.role.name
        )
        user.role = Role.query.filter_by(name='Banned').first()
        db.session.add_all([ban, user])
        db.session.commit()
        return redirect(url_for('.index', username=username))
    return render_template('ban.html', username=username, ban_form=ban_form)


@user.route('/unbanned/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def unbanned(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя нет.', 'alert')
        return redirect(url_for('.index', username=username))
    
    ban = Ban.query.filter_by(user_id=user.id).first()
    if ban is None:
        flash('Пользователь не в бане.', 'alert')
        return redirect(url_for('.index', username=username))

    user.role = Role.query.filter_by(name=ban.last_role).first()
    db.session.add(user)
    db.session.delete(ban)
    db.session.commit()
    return redirect(url_for('.index', username=username))