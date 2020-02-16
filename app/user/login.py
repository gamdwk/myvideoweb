from . import user
from flask import render_template, request, redirect, url_for, flash
from .form import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.urls import url_parse


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter(User.username == username).first()
            if not user:
                flash('用户不存在')
            elif user.checkpassword(password):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            else:
                flash('请检查账户密码是否正确')
    return render_template('user/login.html', form=LoginForm())


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
