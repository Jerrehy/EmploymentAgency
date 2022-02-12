from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired, NumberRange
from agency_app.models import SystemUser


# Форма регистрации на сайте
class RegisterForm(FlaskForm):
    # Проверка наличия совпадений имён пользователей при создании нового пользователя
    def validate_login(self, login_to_check):
        user = SystemUser.get_user_by_login(login_to_check.data)
        if user:
            raise ValidationError('Такое имя пользователя уже есть! Попробуйте придумать другое')

    # Проверка наличия совпадени ФИО при создании нового пользователя
    def validate_fio(self, fio_to_check):
        fio = SystemUser.get_user_by_fio(fio_to_check.data)
        if fio:
            raise ValidationError('У такого человека уже существует аккаунт! '
                                  'Если пароль и логин забыты, то обратитесь к администратору')

    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='ФИО:', validators=[DataRequired()])
    birthday = DateField(label='Дата рождения:', validators=[DataRequired()])
    phone_number = StringField(label='Телефон:')
    role = SelectField(label='Роль на сайте:', choices=[])
    user_photo = StringField(label='Ссылка на фото пользователя с размером близким к 300х300')
    login = StringField(label='Логин:', validators=[Length(min=6, max=20), DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Подтвердить пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


# Форма авторизации на сайте
class LoginForm(FlaskForm):
    login = StringField(label="Логин:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    submit = SubmitField(label='Вход')


# Форма авторизации на сайте
class AddCompany(FlaskForm):
    company_name = StringField(label="Именование компании:", validators=[DataRequired()])
    name_industry = SelectField(label='Индустрия:', choices=[])
    logo = StringField(label="Ссылка на лого:")
    submit_add = SubmitField(label='Добавить')


# Форма регистрации на сайте
class UpdateUserProfile(FlaskForm):
    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='Новое ФИО:')
    birthday = DateField(label='Новая дата рождения:')
    phone_number = StringField(label='Новый телефон:')
    user_photo = StringField(label='Ссылка на новое фото пользователя с размером близким к 300х300')
    submit_update = SubmitField(label='Обновить данные профиля')
