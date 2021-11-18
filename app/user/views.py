from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import user
from .forms import EditProfileForm, EditProfileAdminForm, BanForm
from .. import db, users_upload
from ..models import Comment, User, Role, Permission, Manga, follows, Ban
from ..decorators import admin_required, permission_required

@user.route('/<int:id>')
def index(id):
    user = User.query.get_or_404(id)
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
        return render_template("user.html", user=user, title=user.username, pagination=pagination, show=mode)
    return render_template("user.html", user=user, title=user.username)

@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    edit_profile_form = EditProfileForm()
    if edit_profile_form.validate_on_submit():
        if edit_profile_form.avatar.data:
            forder = str(current_user.id) + "/avatar"
            avatar_name = users_upload.save(edit_profile_form.avatar.data, folder=forder)
            current_user.avatar = avatar_name
        if edit_profile_form.background.data:
            forder = str(current_user.id) + "/background"
            current_user.background = users_upload.save(edit_profile_form.background.data, folder=forder)
        current_user.location = edit_profile_form.location.data
        current_user.name = edit_profile_form.name.data
        current_user.site = edit_profile_form.site.data
        current_user.about_me = edit_profile_form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Профиль обновлен.', 'info')
        return redirect(url_for('.index', id=current_user.id))
    edit_profile_form.location.data = current_user.location
    edit_profile_form.name.data = current_user.name
    edit_profile_form.site.data = current_user.site
    edit_profile_form.about_me.data = current_user.about_me
    return render_template("user_edit.html", edit_profile_form=edit_profile_form, title=current_user.username)

@user.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    edit_profile_admin_form = EditProfileAdminForm(user=user)
    if edit_profile_admin_form.validate_on_submit():
        if edit_profile_admin_form.avatar.data:
            forder = str(user.id) + "/avatar"
            user.avatar = users_upload.save(edit_profile_admin_form.avatar.data, folder=forder)
        if edit_profile_admin_form.background.data:
            forder = str(user.id) + "/background"
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
        return redirect(url_for('.index', id=user.id))
    edit_profile_admin_form.email.data = user.email
    edit_profile_admin_form.username.data = user.username
    edit_profile_admin_form.confirmed.data = user.confirmed
    edit_profile_admin_form.role.data = user.role_id
    edit_profile_admin_form.location.data = user.location
    edit_profile_admin_form.name.data = user.name
    edit_profile_admin_form.site.data = user.site
    edit_profile_admin_form.about_me.data = user.about_me
    return render_template("user_edit_admin.html", edit_profile_admin_form=edit_profile_admin_form, user=user, title=user.username)


@user.route('/follow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    user = User.query.get_or_404(id)
    if current_user.is_following(user):
        flash('Вы уже подписаны.', 'warning')
        return redirect(url_for('.index', id=id))
    current_user.follow(user)
    db.session.commit()
    flash('Вы теперь подписаны на %s.' % user.username, 'success')
    return redirect(url_for('.index', id=id))


@user.route('/unfollow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    user = User.query.get_or_404(id)
    if not current_user.is_following(user):
        flash('Вы не подписаны на данного пользователя.', 'warning')
        return redirect(url_for('.index', id=id))
    current_user.unfollow(user)
    db.session.commit()
    flash('Вы больше не подписаны на %s.' % user.username, 'success')
    return redirect(url_for('.index', id=id))


@user.route('/banned/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def banned(id):
    ban_form = BanForm()
    user = User.query.get_or_404(id)
    ban = Ban.query.filter_by(user_id=user.id).first()

    if ban:
        flash('Пользователь в бане.', 'alert')
        return redirect(url_for('.index', id=id))

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
        return redirect(url_for('.index', id=id))
    return render_template('ban.html', username=user.username, ban_form=ban_form)


@user.route('/unbanned/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def unbanned(id):
    user = User.query.get_or_404(id)
    ban = Ban.query.filter_by(user_id=user.id).first()

    if ban is None:
        flash('Пользователь не в бане.', 'alert')
        return redirect(url_for('.index', id=id))

    user.role = Role.query.filter_by(name=ban.last_role).first()
    db.session.add(user)
    db.session.delete(ban)
    db.session.commit()
    return redirect(url_for('.index', id=id))