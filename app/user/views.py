from app.user import user
from app.helper import random_string
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash, request, current_app
from app.user.form import IconForm, PasswordForm
from app import photos, db
from flask_uploads import IMAGES
from werkzeug.datastructures import CombinedMultiDict
import os
from app.models import User


@user.route('/user/me')
@login_required
def me():
    me = current_user
    videos = current_user.videos
    return render_template('user/user.html', user=me, videos=videos)


@user.route('/user/me/icon', methods=['POST', 'GET'])
@login_required
def icon():
    me = current_user
    form = IconForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            icon = form.icon
            # 保存文件
            suffix = os.path.splitext(icon.data.filename)[1]
            filename = random_string() + suffix
            photos.save(icon.data, name=filename)
            # 删除原头像
            if current_user.icon != 'default_icon.jpg':
                os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
            # 修改数据库
            current_user.icon = filename
            db.session.commit()
            return redirect(url_for('user.me'))
        else:
            flash('提交失败')
    return render_template('user/icon.html', user=me, form=form)


@user.route('/user/me/setpassword', methods=['POST', 'GET'])
@login_required
def password():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.checkpassword(form.password.data):
                current_user.setpassword(form.newpassword.data)
                db.session.commit()
                flash('更改密码成功！')
                return redirect(url_for('user.me'))
            else:
                flash('原密码错误')
        else:
            flash('两次密码输入不一致')
    return render_template('user/password.html', form=form)


@user.route('/user/<int:id>')
@login_required
def show_user(id):
    if id == current_user.id:
        return redirect(url_for('user.me'))
    else:
        u = User.query.filter_by(id=id).first_or_404()
        return render_template('user/user.html', user=u)


@user.route('/user/all/page=<int:page>')
@login_required
def all_user(page=1):
    us = User.query.filter()
    pagination = us.paginate(page=page, per_page=3)
    return render_template('user/alluser.html', pagination=pagination)
