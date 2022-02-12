from flask import render_template, Blueprint, redirect, url_for, session, flash
from agency_app.models import Company, Industry, CompanyHirer
from agency_app.forms import AddCompany
from flask_login import current_user


# Создание узла связанного с компаниями
company = Blueprint('company', __name__, template_folder="templates")


# Просмотр всех доступных компаний в базе
@company.route('/all_companies', methods=['GET', 'POST'])
def company_view():
    # Вывод всех проектов
    all_companies = Company.get_all_companies()
    # Форма для добавления новой компании
    form_add_company = AddCompany()
    # Получение списка отраслей
    industry_for_form = Industry.get_all_industry()
    # Добавление отраслей в форму добавления компании
    form_add_company.name_industry.choices = [i.name_industry for i in industry_for_form]

    # Добавление компании по активации формы добавления
    if form_add_company.validate_on_submit():
        if session['role'] == 2:
            industry_for_add = Industry.get_industry_by_name(form_add_company.name_industry.data)

            if form_add_company.logo.data:
                logo_for_add = form_add_company.logo.data
            else:
                logo_for_add = None

            # Добавление новой компании
            Company.add_company(form_add_company.company_name.data, industry_for_add.id_industry, logo_for_add)

            return redirect(url_for('company.company_view'))
        else:
            flash('Войдите в аккаунт работодателя, чтобы добавить компанию', category='danger')
            return redirect(url_for('company.company_view'))

    return render_template('company/company_list.html', all_companies=all_companies, form_add_company=form_add_company)
