from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from app import app, db
from app.models import User, Content, Banners, BlogPost, Quotes


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')

    # def is_accessible(self):
    #     from app.utils.profiles.login import check_admin
    #     if check_admin() is True:
    #         return True
    #     abort(403)


admin = Admin(app)
admin.add_link(MenuLink(name='Back to site >', url='/#top'))
admin.add_view(MyView(name='Hello 1', endpoint='test1'))
admin.add_view(MyView(name='Hello 2', endpoint='test2'))
admin.add_view(MyView(name='Hello 3', endpoint='test3'))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(Content, db.session))
admin.add_view(ModelView(Banners, db.session))
admin.add_view(ModelView(Quotes, db.session))
