from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import Company
from flask_login import login_required


# Создание узла связанного с компаниями
company = Blueprint('company', __name__, template_folder="templates")


# Просмотр всех доступных компаний в базе
@company.route('/all_companies', methods=['GET', 'POST'])
def company_view():
    # Вывод всех проектов
    all_companies = Company.get_all_companies()
    return render_template('company/company_list.html', all_companies=all_companies)
