from app import db, bcrypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), unique=True, index=True, default=username)
    password_hash = db.Column(db.String(64))
    icon = db.Column(db.String(64), default='default_icon.jpg')
    videos = db.relationship("Video", backref='users', lazy='dynamic')
    collect = db.relationship("Video")
    like = db.relationship("Video")
    comments = db.relationship('Comment', backref='users', lazy='dynamic')
    role = db.Column(db.String(64))

    def setpassword(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def checkpassword(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return 'User %r' % self.username

    def is_like(self, video_id):
        for like in self.like:
            if like.id == video_id:
                return True
        return False

    def is_collect(self, video_id):
        for collect in self.collect:
            if collect.id == video_id:
                return True
        return False

    def is_admin(self):
        if self.role == 'admin':
            return True
        return False


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64))
    body = db.Column(db.String(64))
    like = db.Column(db.Integer, default=0)
    collected = db.Column(db.Integer, default=0)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    comments = db.relationship('Comment', backref='videos', lazy='dynamic')

    def __repr__(self):
        return 'Video %r' % self.title

    def get_id(self):
        return str(self.id)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    videos = db.relationship('Video', backref='tag', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))

    def getuser(self):
        return User.query.get(self.user_id)

    def get_id(self):
        return str(self.id)
