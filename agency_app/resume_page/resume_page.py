from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import Resume
from agency_app.forms import AddResume
from flask_login import current_user, login_required


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
