from . import user
from flask import render_template, request, redirect, url_for, flash
from .form import RegisterForm
from .. import db
from app.models import User


@user.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            if User.query.filter_by(username=username).first():
                flash('用户名已存在')
            else:
                try:
                    user = User()
                    user.username = username
                    user.role = 'common_user'
                    user.setpassword(password)
                    db.session.add(user)
                    db.session.commit()
                    flash('注册成功')
                    return redirect(url_for('user.login'))
                except Exception as e:
                    db.session.rollback()
                    flash('注册失败')
    return render_template('user/register.html', form=form)
