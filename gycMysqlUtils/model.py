from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
# 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名jianshu,连接方式参考 \
#  http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:guyuchao@127.0.0.1:3306/imgprocess'
#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True #实例化
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password=password

    def __repr__(self):
        return '<User %r>' % self.username

class Img(db.Model):
    __tablename__ = 'img'
    imgid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), unique=True)

    def __init__(self, filename):
        self.filename=filename

    def __repr__(self):
        return '<Img %r>' % self.filename

class UserImg(db.Model):
    __tablename__ = 'userimg'
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'),primary_key=True)
    imgid = db.Column(db.Integer, db.ForeignKey('img.imgid'),primary_key=True)
    filename=db.Column(db.String(50),unique=True)

    def __init__(self, userid,imgid,filename):
        self.userid=userid
        self.imgid=imgid
        self.filename=filename

    def __repr__(self):
        return '<UserImg %r,%r>' % self.userid,self.imgid,self.filename

#db.create_all()
