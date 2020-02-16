from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class

db = SQLAlchemy()
bcrypt = Bcrypt()
lm = LoginManager()
photos = UploadSet('PHOTOS', IMAGES)
videos = UploadSet('VIDEOS')


def creatapp(config):
    app = Flask(__name__)
    app.config.from_object(config)
    bcrypt.init_app(app)
    lm.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)
    configure_uploads(app, videos)
    patch_request_class(app, size=None)
    return app


app = creatapp('config')

from app.user import user as userBlueprint
from app.video import video as videoBlueprint
from app.admin import admin as adminBlueprint

app.register_blueprint(userBlueprint)
app.register_blueprint(videoBlueprint)
app.register_blueprint(adminBlueprint)
db.create_all(app=app)
from app.dbinit import creatags, Tags, creatadmin

creatags(Tags)
creatadmin()
from . import views, models

from app.models import User


@lm.user_loader
def loader_user(id):
    return User.query.get(int(id))
