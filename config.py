CSRF_ENABLED = True  # 激活跨站点请求伪造保护
SECRET_KEY = 'stn-boo'

# 配置flask_sqlalchemy
username = 'root'
password = '123888.hh'
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + username + ':' + password + '@localhost:3306/videoweb?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 配置flask-uploads
from os import path
from flask_uploads import IMAGES

# photos的配置
UPLOADED_PHOTOS_DEST = path.join(path.dirname(path.abspath(__file__)),
                                 "app\\static\\pic\\userhead")  # 配置文件保存的目录，本参数必须设置
UPLOADED_PHOTOS_ALLOW = IMAGES  # 配置允许的扩展名，其他的都是不允许
UPLOADED_PHOTOS_DENY = ['html']  # 配置不允许的扩展名
# videos的配置
UPLOADED_VIDEOS_DEST = path.join(path.dirname(path.abspath(__file__)),
                                 "app\\static\\video")
UPLOADED_VIDEOS_ALLOW = ['mp4', 'avi', 'mov', 'flv', 'wmv']
if __name__ == '__main__':
    print(UPLOADED_PHOTOS_DEST)