from flask_user import UserMixin
import app


class User(app.db.Model, UserMixin):

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
