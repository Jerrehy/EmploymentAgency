from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import Resume, SystemUser
from flask_login import login_required, current_user


# Создание узла связанного с вакансиями
resume = Blueprint('resume', __name__, template_folder="templates")


# Просмотр информации о пользователе
@resume.route('/resume_view', methods=['GET'])
@login_required
def resume_view():
    if session['role'] == 2:
        all_resume = Resume.get_all_resume()
        return render_template('resume/resume_list.html', all_resume=all_resume)
    else:
        flash('У вас недостаточно прав для просмотра этой страницы')
        return redirect(url_for('start.begin_page'))


# Просмотр информации о пользователе
@resume.route('/personal_resume_view', methods=['GET'])
@login_required
def personal_resume_view():
    if session['role'] != 2:
        activated_user = SystemUser.get_user_by_login_with_role(session['login'])
        all_my_resume = Resume.get_all_resume_by_id(current_user.get_id())
        return render_template('resume/user_resume.html', all_my_resume=all_my_resume, activated_user=activated_user)
    else:
        flash('У вас недостаточно прав для просмотра этой страницы')
        return redirect(url_for('start.begin_page'))
