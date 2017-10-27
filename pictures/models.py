from pictures import db
from datetime import datetime
from pictures import login_manager
from flask_login import UserMixin, AnonymousUserMixin
import random,hashlib
from flask import flash,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Uncomfired':(Permission.FOLLOW,True),
            'User':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES,False),
            'Moderate':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS,False),
            'Adminstrator':(Permission.ADMINISTER,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(20))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image',backref='user',lazy='dynamic')
    comments = db.relationship('Comment',backref='user',lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


    def __init__(self,username,password,email=None,status=0):
        self.username = username
        self.password = password
        self.email = email
        if self.role_id == None:
            self.role_id == Role.query.filter_by(default=1).first().id

    def __repr__(self):
        return '<User %r>' %self.username

    # @property
    # def head_url(self):
    #     return self.head_url

    # create default salt for new user
    @staticmethod
    def get_salt():
        salt = '.'.join(random.sample('this0is1a2python3program4to5show6picture7', 10))
        return salt

    # encrypt the password
    @staticmethod
    def md5_for_password(password, salt):
        m = hashlib.md5((password + salt).encode("utf8"))
        password = m.hexdigest()
        return password

    # check if the username and password match
    @staticmethod
    def check_user(email, password):
        user = User.query.filter_by(email=email).first()
        # print('this is the email: ',email)
        if user == None:
            return flash('unknown email !')
        password = User.md5_for_password(password, user.salt)
        if user.password != password:
            return flash('unknown email or bad password !')
        return user

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

#load user for flask-login
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

class Image(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    comments = db.relationship('Comment',backref='image',lazy='dynamic')

    def __init__(self,url,user_id = 10):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' %(self.id,self.url)

    # show the last 5 pictures for index page
    @staticmethod
    def show_images(page=1, per_page=5):
        images = Image.query.paginate(page, per_page).items
        return images

    # load the image by id
    @staticmethod
    def image_by_id(imageId):
        image = Image.query.filter_by(id=imageId).first()
        return image


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    status = db.Column(db.Integer,default=0) #

    def __init__(self,image_id,user_id,content):
        self.user_id = user_id
        self.image_id = image_id
        self.content = content
        self.create_date = datetime.now()

    def __repr__(self):
        return '<Comment %d %s>' %(self.id,self.content)

