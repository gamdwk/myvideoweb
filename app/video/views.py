from app.video import video
from flask import render_template, request, flash, current_app, jsonify
from app import db, videos
from .form import VideoUploadForm, CommentForm
from app.models import Video, Tag, Comment
from flask_login import current_user
from app.helper import random_string
from flask_login import login_required
import os


@video.route('/video/<int:id>/page=<int:page>', methods=['POST', 'GET'])
def show_video(id, page=1):
    v = Video.query.filter_by(id=id).first_or_404()
    folder = str(v.user_id) + '/'
    filename = 'video/' + folder + v.body
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                comment = Comment()
                comment.body = form.comment.data
                comment.user_id = current_user.id
                comment.video_id = id
                db.session.add(comment)
                db.session.commit()
                flash('发表成功')
            except:
                db.session.rollback()
                flash('发表失败')
        else:
            flash('发表失败')
    pagination = v.comments.paginate(page=page, per_page=5)
    tag = Tag.query.filter_by(id=v.tag_id).first().name
    return render_template(
        'video/video.html', filename=filename, form=form,tag = tag,
        pagination=pagination, id=id, video=v)


@video.route('/video/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoUploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                suffix = os.path.splitext(form.video.data.filename)[1]
                filename = random_string() + suffix
                videos.save(form.video.data, folder=str(current_user.id), name=filename)
                v = Video()
                v.title = form.title.data
                v.body = filename
                v.user_id = current_user.id
                v.tag_id = int(Tag.query.filter_by(name=str(form.tag.data)).first().id)
                db.session.add(v)
                db.session.commit()
                flash('上传成功')
            except Exception as e:
                db.session.rollback()
                flash('上传失败，请稍后再试')
        else:
            flash('格式错误')
    return render_template('video/upload.html', form=form)


@video.route('/video/delete', methods=['GET', 'POST'])
@login_required
def delete():
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
    return render_template('video/delete.html', videos=current_user.videos)


@video.route('/me/all_video/?page=<int:page>')
@login_required
def all_video(page=1):
    vs = current_user.videos
    pagination = vs.paginate(page=page, per_page=3)
    return render_template('video/allvideo.html', pagination=pagination)


@video.route('/all_video/page=<int:page>')
def show_all_video(page=1):
    vs = Video.query.filter()
    pagination = vs.paginate(page=page, per_page=3)
    return render_template('video/allvideo.html', pagination=pagination)


@video.route('/video/make_likes')
@login_required
def make_likes():
    result = {'code': ''}
    if request.method == 'POST':
        try:
            like = int(request.form.get('like'))
            id = int(request.form.get('id'))
            v = Video.query.get_or_404(id)
            v.like = v.like + like
            if like == 1:
                current_user.like.add(v.id)
            elif current_user.is_collect(v.id):
                current_user.like.remove(v)
            else:
                current_user.like.add(v.id)
            db.session.commit()
            result['code'] = 200
        except:
            db.session.rollback()
            result['code'] = 400

        return jsonify(result)
