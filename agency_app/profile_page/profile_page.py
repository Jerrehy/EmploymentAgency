from flask import render_template, Blueprint, redirect, url_for, session
from agency_app.models import SystemUser, Company, CompanyHirer
from agency_app.forms import UpdateUserProfile, CompanyBinding
from flask_login import login_required, current_user


# Создание узла связанного с профилем и его изменением
profile = Blueprint('profile', __name__, template_folder="templates")


# Просмотр информации о пользователе
@profile.route('/profile_view', methods=['GET', 'POST'])
@login_required
def profile_view():

    # Выборка вывода информации в зависимости от наличия пользователя в таблице с привязкой к компании
    if CompanyHirer.get_hirer_by_id(current_user.get_id()):
        activated_user = SystemUser.get_user_by_login_with_role_and_hiring(session['login'])
    else:
        activated_user = SystemUser.get_user_by_login_with_role(session['login'])

    # Форма для привязки работодателя к компании
    company_binding_form = CompanyBinding()
    # Выбор списка компаний и заполнение формы привязки этим списком
    company_list = Company.get_all_companies()
    company_binding_form.company_name.choices = [i.Company.name_company for i in company_list]

    if company_binding_form.submit_binding.data:
        # Поиск компании по названию
        company_for_binding = Company.get_company_by_name(company_binding_form.company_name.data)
        # Добавление привязки
        CompanyHirer.add_company_hirer(company_for_binding.id_company, current_user.get_id())
        return redirect(url_for('profile.profile_view'))

    return render_template('profile/user_profile.html', activated_user=activated_user,
                           company_binding_form=company_binding_form)


# Обновление профиля пользователя
@profile.route('/update_profile_view', methods=['GET', 'POST'])
@login_required
def profile_update_view():
    # Форма для обновления профиля
    update_profile_form = UpdateUserProfile()
    # Получение текущей информации о пользователе
    activated_user = SystemUser.get_user_by_login(session['login'])

    if update_profile_form.submit_update.data:
        # Проверка на введённые в форме данные

        # ФИО
        if update_profile_form.fio.data:
            fio = update_profile_form.fio.data
        else:
            fio = activated_user.fio
        # Дата рождения
        if update_profile_form.birthday.data:
            birthday = update_profile_form.fio.data
        else:
            birthday = activated_user.birthday
        # Номер телефона
        if update_profile_form.phone_number.data:
            phone_number = update_profile_form.phone_number.data
        else:
            phone_number = activated_user.phone_number
        # Фото пользователя
        if update_profile_form.user_photo.data:
            photo = update_profile_form.user_photo.data
        else:
            photo = activated_user.photo

        # Обновление профиля пользователя
        SystemUser.update_system_user(session['login'], fio, phone_number, birthday, photo)

        return redirect(url_for('profile.profile_view'))

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)
