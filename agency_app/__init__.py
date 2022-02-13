from flask import Flask
from agency_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# Подключение шифратора для паролей
bcrypt = Bcrypt(app)

# Настройка пользовательского входа с помощь логин менеджера
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключение узлов с методами к приложению
from agency_app.start_page.start_page import start
from agency_app.authentication.authentication import authentication
from agency_app.company_page.company_page import company
from agency_app.industry_positions_page.industry_positions_page import industry_positions
from agency_app.profile_page.profile_page import profile
from agency_app.vacancy_page.vacancy_page import vacancy
from agency_app.resume_page.resume_page import resume

app.register_blueprint(start)
app.register_blueprint(authentication)
app.register_blueprint(company)
app.register_blueprint(industry_positions)
app.register_blueprint(profile)
app.register_blueprint(vacancy)
app.register_blueprint(resume)
