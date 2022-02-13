from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import Resume, SystemUser, JobPosition
from agency_app.forms import AddResume
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
@resume.route('/personal_resume_view', methods=['GET', 'POST'])
@login_required
def personal_resume_view():
    if session['role'] != 2:
        activated_user = SystemUser.get_user_by_login_with_role(session['login'])
        all_my_resume = Resume.get_all_resume_by_id(current_user.get_id())

        add_resume_form = AddResume()
        positions_for_personal_view = JobPosition.get_all_job_positions()
        add_resume_form.name_job_position.choices = [i.name_job_position for i in positions_for_personal_view]

        if add_resume_form.submit_add.data:
            positions_for_personal_add = JobPosition.get_job_positions_by_name(add_resume_form.name_job_position.data)
            Resume.add_resume(current_user.get_id(), add_resume_form.education.data, add_resume_form.work_experience.data,
                              positions_for_personal_add.id_job_position)
            return redirect(url_for('resume.personal_resume_view'))

        return render_template('resume/user_resume.html', all_my_resume=all_my_resume, activated_user=activated_user,
                               add_resume_form=add_resume_form)
    else:
        flash('У вас недостаточно прав для просмотра этой страницы')
        return redirect(url_for('start.begin_page'))
