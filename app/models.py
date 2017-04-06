import app
import datetime
from sqlalchemy import DateTime


class User(app.db.Model):
    """ A user who has an account on the website. """

    id = app.db.Column(app.db.Integer, primary_key=True)

    name = app.db.Column(app.db.String(64),
                         nullable=False,
                         server_default='Anonymous User')

    is_admin = app.db.Column(app.db.Boolean(),
                             nullable=False,
                             default=False)

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_admin(self):
        return self.is_admin


class Role(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    name = app.db.Column(app.db.String(50), unique=True)


class UserRoles(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    user_id = app.db.Column(app.db.Integer(),
                            app.db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = app.db.Column(app.db.Integer(),
                            app.db.ForeignKey('role.id', ondelete='CASCADE'))


class Content(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    title = app.db.Column(app.db.String(140), nullable=False)
    content = app.db.Column(app.db.Text(), nullable=False)
    image_url = app.db.Column(app.db.Text())
    key = app.db.Column(app.db.String(60), nullable=False, unique=True)


class Banners(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    image_url = app.db.Column(app.db.Text())

    def __init__(self, image_url):
        self.image_url = image_url


class UserBlogPosts(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    title = app.db.Column(app.db.String(140), nullable=False)
    text = app.db.Column(app.db.NVARCHAR(), nullable=False)
    image_url = app.db.Column(app.db.Text())
    filter = app.db.Column(app.db.String(60), default='GENERAL', nullable=False)
    user = app.db.Column(app.db.String(140), nullable=False)
    datetime = app.db.Column(DateTime, default=datetime.datetime.utcnow)
    user_id = app.db.Column(app.db.String(140), nullable=False)
    viewable = app.db.Column(app.db.Boolean(),
                             nullable=False,
                             default=False)

    def __init__(self, title, text, image_url, filter, user, user_id):
        self.title = title
        self.text = text
        self.image_url = image_url
        self.filter = filter
        self.user = user
        self.user_id = user_id
        from app.utils.profiles.login import check_admin
        if check_admin():
            self.viewable = True


class Quotes(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    quote = app.db.Column(app.db.String(140), nullable=False)


class Committee(app.db.Model):
    id = app.db.Column(app.db.Integer(), primary_key=True)
    role = app.db.Column(app.db.String(140), nullable=False)
    name = app.db.Column(app.db.String(140), nullable=False)
    text = app.db.Column(app.db.Text(), nullable=False)
    photo = app.db.Column(app.db.Text(), nullable=False)

    def getRole(self):
        return self.role

    def getName(self):
        return self.name
