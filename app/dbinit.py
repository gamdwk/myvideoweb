from app import db, app
from app.models import Tag, User

Tags = ['game', 'life', 'movie', 'music', 'else']


def creatags(tags):
    with app.app_context():
        for tag in tags:
            try:
                t = Tag()
                t.name = tag
                db.session.add(t)
                db.session.commit()
            except:
                db.session.rollback()


def creatadmin():
    with app.app_context():
        try:
            admin = User()
            admin.role = 'admin'
            admin.username = 'admin'
            admin.setpassword('root')
            db.session.add(admin)
            db.session.commit()
        except:
            db.session.rollback()
