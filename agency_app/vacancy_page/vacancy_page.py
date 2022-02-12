from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import JobVacancy, CompanyHirer, JobPosition
from agency_app.forms import AddVacancy
from flask_login import current_user


# Создание узла связанного с вакансиями
vacancy = Blueprint('vacancy', __name__, template_folder="templates")


# Просмотр информации о пользователе
@vacancy.route('/vacancy_view', methods=['GET', 'POST'])
def vacancy_view():
    all_vacancy = JobVacancy.get_all_vacancy()
    add_form_vacancy = AddVacancy()
    company_user = CompanyHirer.get_hirer_by_id(current_user.get_id())

    list_positions = JobPosition.get_all_job_positions()
    add_form_vacancy.name_job_position.choices = [i.name_job_position for i in list_positions]

    if add_form_vacancy.submit_add.data:
        if session['role'] == 2:
            if company_user:
                job_pos_for_add = JobPosition.get_job_positions_by_name(add_form_vacancy.name_job_position.data)
                JobVacancy.add_vacancy(current_user.get_id(), company_user.id_company, job_pos_for_add.id_job_position,
                                       add_form_vacancy.salary.data)
                return redirect(url_for('vacancy.vacancy_view'))
            else:
                flash('Выберите компанию в профиле, пройдя авторизацию', category='danger')
                return redirect(url_for('start.begin_page'))
        else:
            flash('Вы не работодатель. Зайдите в свой аккаунт', category='danger')
            return redirect(url_for('vacancy.vacancy_view'))

    return render_template('vacancy/vacancy_list.html', all_vacancy=all_vacancy, add_form_vacancy=add_form_vacancy)
