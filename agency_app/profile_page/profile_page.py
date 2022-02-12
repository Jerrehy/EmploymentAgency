from flask import render_template, Blueprint, redirect, url_for, session, flash
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
    activated_user = SystemUser.get_user_by_login_with_role(session['login'])

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)
