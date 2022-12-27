from flask import Flask, render_template, request, redirect, abort
from flask_admin import Admin
from flask_login import LoginManager, login_user
from uuid import uuid4


from app.db.session import SyncSession, scope
from app.core.config import settings

from app.admin.views.tg_user import TelegramUserView
from app.admin.views.application import ApplicationView
from app.admin.views.users import UsersViews

from app.models.user import User
from app.models.telegram_user import TelegramUser
from app.models.application import Application


from loguru import logger

session = SyncSession(settings.SYNC_SQLALCHEMY_DATABASE_URI)


secureApp = Flask(__name__)
login = LoginManager(secureApp)


@login.user_loader
def load_user(user_id):
    return session.session.query(User).filter(User.id == user_id).first()


secureApp.config['SECRET_KEY'] = 'secretkey'


class Middleware:
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scope.set(str(uuid4()))
        try:
            return self.app(environ, start_response)
        except Exception as _exc:
            print(_exc)
            session.session.rollback()
        finally:
            session.session.expunge_all()
            session.scoped_session.remove()


secureApp.wsgi_app = Middleware(secureApp.wsgi_app)


# create administrator
admin = Admin(secureApp, name='Admin', base_template='my_master.html', template_mode='bootstrap4')
# Add view
admin.add_view(TelegramUserView(TelegramUser, session.session))
admin.add_view(ApplicationView(Application, session.session))
admin.add_view(UsersViews(User, session.session))


@secureApp.route("/admin/login/", methods=['POST', 'GET'])
def login():
    logger.info("in func")
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = session.session.query(User).filter(
            User.password == password,
            User.login == login
        ).first()
        if user.is_active:
            logger.info("go to login")
            login_user(user)
        return redirect('/admin')
    else:
        return render_template('index.html')
