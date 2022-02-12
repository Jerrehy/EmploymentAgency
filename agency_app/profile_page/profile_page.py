from flask import render_template, Blueprint, redirect, url_for, session
from agency_app.models import SystemUser
from agency_app.forms import UpdateUserProfile
from flask_login import login_required


# Создание узла связанного с профилем и его изменением
profile = Blueprint('profile', __name__, template_folder="templates")


# Просмотр информации о пользователе
@profile.route('/profile_view', methods=['GET', 'POST'])
@login_required
def profile_view():
    activated_user = SystemUser.get_user_by_login_with_role(session['login'])
    return render_template('profile/user_profile.html', activated_user=activated_user)


# Обновление профиля пользователя
@profile.route('/update_profile_view', methods=['GET', 'POST'])
@login_required
def profile_update_view():

    update_profile_form = UpdateUserProfile()
    activated_user = SystemUser.get_user_by_login(session['login'])

    if update_profile_form.submit_update.data:
        # Проверка на введённые в форме данные
        if update_profile_form.fio.data:
            fio = update_profile_form.fio.data
        else:
            fio = activated_user.fio

        if update_profile_form.birthday.data:
            birthday = update_profile_form.fio.data
        else:
            birthday = activated_user.birthday

        if update_profile_form.phone_number.data:
            phone_number = update_profile_form.phone_number.data
        else:
            phone_number = activated_user.phone_number

        if update_profile_form.user_photo.data:
            photo = update_profile_form.fio.data
        else:
            photo = activated_user.photo

        # Обновление пользователя
        SystemUser.update_system_user(session['login'], fio, phone_number, birthday, photo)

        return redirect(url_for('profile.profile_view'))

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)
