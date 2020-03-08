from . import admin
from app import db
from app.models import User, Video, Comment
from flask_login import login_required
from flask import current_app, abort, render_template, redirect, request, flash
import os
from flask_login import current_user


@admin.route('/admin/base')
@login_required
def base():
    if current_user.is_admin():
        return render_template('admin/adminbase.html', user='管理员')
    else:
        return render_template('admin/adminbase.html', user='普通用户')


@admin.route('/admin/user/page=<int:page>', methods=['POST', 'GET'])
@login_required
def user(page=1):
    if current_user.is_admin():
        if request.method == 'POST':
            u_ids = request.values.getlist('select')
            for u_id in u_ids:
                u = User.query.get(int(u_id))
                try:
                    if request.values.get('sub')=="批量删除":
                        db.session.delete(u)
                        db.session.commit()
                        flash(u.username + '删除成功')
                    else:
                        u.role = 'admin'
                        db.session.commit()
                        flash(u.username + '设置成功')
                except Exception as e:
                    db.session.rollback()
                    flash(u.username + '失败')
        pagination = User.query.filter().paginate(page=page, per_page=5)
        return render_template('admin/useradmin.html', pagination=pagination)
    else:
        abort(404)


@admin.route('/admin/video/page=<int:page>', methods=['POST', 'GET'])
@login_required
def video(page=1):
    if current_user.is_admin():
        if request.method == 'POST':
            v_ids = request.values.getlist('select')
            for v_id in v_ids:
                v = Video.query.get(int(v_id))
                try:
                    db.session.delete(v)
                    os.remove(
                        os.path.join(current_app.config['UPLOADED_VIDEOS_DEST'], str(v.user_id) + '/' + v.body))
                    db.session.commit()
                    flash(v.title + '删除成功')
                except Exception as e:
                    db.session.rollback()
                    flash(v.title + '删除失败')
        pagination = Video.query.filter().paginate(page=page, per_page=5)
        return render_template('admin/videoadmin.html', pagination=pagination)
    else:
        if request.method == 'POST':
            v_ids = request.values.getlist('select')
            for v_id in v_ids:
                v = Video.query.get(int(v_id))
                try:
                    db.session.delete(v)
                    os.remove(
                        os.path.join(current_app.config['UPLOADED_VIDEOS_DEST'], current_user.get_id() + '/' + v.body))
                    db.session.commit()
                    flash(v.title + '删除成功')
                except Exception as e:
                    db.session.rollback()
                    flash(v.title + '删除失败')
        pagination = current_user.videos.paginate(page=page, per_page=5)
        return render_template('admin/videoadmin.html', pagination=pagination)


@admin.route('/admin/comment/id=<int:id>/page=<int:page>', methods=['POST', 'GET'])
@login_required
def comment(id, page=1):
    if current_user.is_admin():
        if request.method == 'POST':
            c_ids = request.values.getlist('select')
            for c_id in c_ids:
                c = Comment.query.get(int(c_id))
                try:
                    db.session.delete(c)
                    db.session.commit()
                    flash('删除成功')
                except Exception as e:
                    db.session.rollback()
                    flash('删除失败')
        pagination = Video.query.filter_by(id=id).first().comments.paginate(page=page, per_page=5)
        return render_template('admin/commentadmin.html', pagination=pagination, id=id)
    else:
        if request.method == 'POST':
            c_ids = request.values.getlist('select')
            for c_id in c_ids:
                c = Video.query.get(int(c_id))
                try:
                    db.session.delete(c)
                    db.session.commit()
                    flash('删除成功')
                except Exception as e:
                    db.session.rollback()
                    flash('删除失败')
        pagination = current_user.comments.paginate(page=page, per_page=5)
        return render_template('admin/commentadmin.html', pagination=pagination, id=id)
