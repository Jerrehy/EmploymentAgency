from flask_login import UserMixin
from agency_app import db
from agency_app import bcrypt
from agency_app import login_manager
from flask import flash


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return SystemUser.query.get(int(user_id))


# Таблица со списком компаний
class Company(db.Model):
    __tablename__ = 'company'
    __table_args__ = {'extend_existing': True}

    # Просмотр всех компаний
    @staticmethod
    def get_all_companies():
        query = db.session.query(Company, Industry)
        query = query.outerjoin(Industry, Company.id_industry == Industry.id_industry)
        return query.all()

    # Просмотр информации о компании по её именованию
    @staticmethod
    def get_company_by_name(name_company):
        Company.query.filter_by(name_company=name_company).first()

    # Добавление новой компании
    @staticmethod
    def add_company(name_company, id_industry, logo=None):
        new_company = Company(name_company=name_company, id_industry=id_industry, logo=logo)

        try:
            db.session.add(new_company)
            db.session.commit()
            flash("Добавление новой компании", category='success')
        except:
            db.session.rollback()
            flash("Ошибка при добавлении новой компании", category='danger')


# Таблица принадлежности работодателей к компании
class CompanyHirer(db.Model):
    __tablename__ = 'company_hirer'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_company_hirer(id_company, id_hirer):
        new_company_hirer = CompanyHirer(id_company=id_company, id_hirer=id_hirer)

        try:
            db.session.add(new_company_hirer)
            db.session.commit()
            flash("Добавление нового работодателя в компании", category='success')
        except:
            db.session.rollback()
            flash("Ошибка привязк нового работодателя к компании", category='danger')


# Таблица всех отраслей
class Industry(db.Model):
    __tablename__ = 'industry'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех отраслей
    @staticmethod
    def get_all_industry():
        return Industry.query.all()

    # Метод получения информации об индустрии по её названию
    @staticmethod
    def get_industry_by_name(name_industry):
        return Industry.query.filter_by(name_industry=name_industry).first()


# Таблица всех доступных должностей
class JobPosition(db.Model):
    __tablename__ = 'job_position'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_job_positions():
        return JobPosition.query.all()


class JobVacancy(db.Model):
    __tablename__ = 'job_vacancy'
    __table_args__ = {'extend_existing': True}


class Resume(db.Model):
    __tablename__ = 'resume'
    __table_args__ = {'extend_existing': True}


# Таблица с ролями пользователей
class RoleUser(db.Model):
    __tablename__ = 'role_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_roles():
        return RoleUser.query.all()

    @staticmethod
    def get_role_by_name(name_role_user):
        return RoleUser.query.filter_by(name_role_user=name_role_user).first()


# Таблица с пользователями системы
class SystemUser(db.Model, UserMixin):
    __tablename__ = 'system_user'
    __table_args__ = {'extend_existing': True}

    id_system_user = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_system_user

    # Получени пароля
    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    # Шифрование пароля
    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Проверка пароля
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    # Получение информации о пользователе по логину
    @staticmethod
    def get_user_by_login_with_role(login):
        query = db.session.query(SystemUser, RoleUser)
        query = query.join(RoleUser, SystemUser.id_role_user == RoleUser.id_role_user)
        query = query.filter(SystemUser.login == login )
        return query.first()

    # Получение информации о пользователе по логину
    @staticmethod
    def get_user_by_login(login):
        return SystemUser.query.filter_by(login=login).first()

    # Получение информации о пользователе по фамилии
    @staticmethod
    def get_user_by_fio(fio):
        return SystemUser.query.filter_by(fio=fio).first()

    # Изменение данных о пользователе
    @staticmethod
    def update_system_user(login, fio, phone_number, birthday, photo):
        try:
            user_for_update = SystemUser.get_user_by_login(login)

            user_for_update.fio = fio
            user_for_update.phone_number = phone_number
            user_for_update.birthday = birthday
            user_for_update.photo = photo

            db.session.commit()
            flash("Пользователь был успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при изменнии пользователя. Повторите попытку.", category='danger')

    # Добавление нового пользователя
    @staticmethod
    def add_system_user(fio, phone_number, birthday, login, password, id_role_user, photo=None):
        new_system_user = SystemUser(fio=fio, phone_number=phone_number, birthday=birthday, login=login,
                                     unencrypted_password=password, id_role_user=id_role_user, photo=photo)

        try:
            db.session.add(new_system_user)
            db.session.commit()
            flash("Пользователь был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении пользователя. Повторите попытку.", category='danger')
