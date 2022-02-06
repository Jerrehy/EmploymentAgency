from flask_login import UserMixin
from agency_app import db
from agency_app import bcrypt
from agency_app import login_manager
from flask import flash


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return SystemUser.query.get(int(user_id))


class Company(db.Model):
    __tablename__ = 'company'
    __table_args__ = {'extend_existing': True}


class CompanyHirer(db.Model):
    __tablename__ = 'company_hirer'
    __table_args__ = {'extend_existing': True}


class Industry(db.Model):
    __tablename__ = 'industry'
    __table_args__ = {'extend_existing': True}


class JobPosition(db.Model):
    __tablename__ = 'job_position'
    __table_args__ = {'extend_existing': True}


class JobVacancy(db.Model):
    __tablename__ = 'job_position'
    __table_args__ = {'extend_existing': True}


class Resume(db.Model):
    __tablename__ = 'resume'
    __table_args__ = {'extend_existing': True}


class RoleUser(db.Model):
    __tablename__ = 'role_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_roles():
        return RoleUser.query.all()

    @staticmethod
    def get_role_by_name(name_role_user):
        return RoleUser.query.filter_by(name_role_user=name_role_user).first()


class SystemUser(db.Model, UserMixin):
    __tablename__ = 'system_user'
    __table_args__ = {'extend_existing': True}

    id_system_user = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_system_user

    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    @staticmethod
    def get_user_by_login(login):
        return SystemUser.query.filter_by(login=login).first()

    @staticmethod
    def get_user_by_fio(fio):
        return SystemUser.query.filter_by(login=fio).first()

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
