from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import JobVacancy, CompanyHirer, JobPosition
from agency_app.forms import AddVacancy, DelVacancy
from flask_login import current_user, login_required

# Создание узла связанного с вакансиями
vacancy = Blueprint('vacancy', __name__, template_folder="templates")


# Просмотр все доступных вакансий
@vacancy.route('/vacancy_view', methods=['GET', 'POST'])
def vacancy_view():
    # Список всех вакансий
    all_vacancy = JobVacancy.get_all_vacancy()
    return render_template('vacancy/vacancy_list.html', all_vacancy=all_vacancy)


# Просмотр все доступных вакансий, созданных работодателем
@vacancy.route('/vacancy_hirer_view', methods=['GET', 'POST'])
@login_required
def vacancy_hirer_view():
    if session['role'] == 2:
        # Форма для добавления вакансии
        add_form_vacancy = AddVacancy()
        # Форма для удаления вакансии
        del_form_vacancy = DelVacancy()
        # Получение информации о текущем работодателе
        company_user = CompanyHirer.get_hirer_by_id(current_user.get_id())
        # Список всех вакансий
        all_vacancy = JobVacancy.get_all_vacancy(company_user.id_hirer)

        # Получения списка всех должностей и внесение в форму добавления
        list_positions = JobPosition.get_all_job_positions()
        add_form_vacancy.name_job_position.choices = [i.name_job_position for i in list_positions]

        # Добавление вакансии за работодателя по кнопке
        if add_form_vacancy.submit_add.data:
            if company_user:
                job_pos_for_add = JobPosition.get_job_positions_by_name(add_form_vacancy.name_job_position.data)
                JobVacancy.add_vacancy(current_user.get_id(), company_user.id_company, job_pos_for_add.id_job_position,
                                       add_form_vacancy.salary.data)
                return redirect(url_for('vacancy.vacancy_hirer_view'))
            else:
                flash('Выберите компанию в профиле, пройдя авторизацию', category='danger')
                return redirect(url_for('start.begin_page'))

        # Удаление вакансии работодателя по кнопке
        elif del_form_vacancy.submit_del.data:
            JobVacancy.del_vacancy(del_form_vacancy.id_vacancy.data)
            return redirect(url_for('vacancy.vacancy_hirer_view'))

        return render_template('vacancy/vacancy_hirer_list.html', all_vacancy=all_vacancy,
                               add_form_vacancy=add_form_vacancy, del_form_vacancy=del_form_vacancy)
    else:
        flash('У вас нет прав для просмотра этой страницы', category='danger')
        return redirect(url_for('start.begin_page'))
