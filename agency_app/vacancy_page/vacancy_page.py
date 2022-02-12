from flask import render_template, Blueprint, redirect, url_for, session
from agency_app.models import JobVacancy
from agency_app.forms import UpdateUserProfile
from flask_login import login_required


# Создание узла связанного с вакансиями
vacancy = Blueprint('vacancy', __name__, template_folder="templates")


# Просмотр информации о пользователе
@vacancy.route('/vacancy_view', methods=['GET'])
def vacancy_view():
    all_vacancy = JobVacancy.get_all_vacancy()
    return render_template('vacancy/vacancy_list.html', all_vacancy=all_vacancy)
