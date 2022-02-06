from flask import Blueprint, render_template
# from agency_app.models import
# from agency_app.forms import
# from flask_login import login_required, current_user

start = Blueprint('start', __name__, template_folder="templates")


# Начальная страница сайта
@start.route('/')
@start.route('/main', methods=['GET'])
def begin_page():
    return render_template('start/main.html')


# # Страница профиля пользователя
# # Декоратор @login_required для доступа к странице
# @user.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile_page():
#     # Получение информации о пользователе по ID сессии
#     employer = Employee.get_employee_by_id(current_user.get_id())
#     # Подключение формы для изменения профиля пользователя
#     form_for_employee = EmployeeUpdate()
#
#     # Модуль для изменения профиля пользователя
#     if form_for_employee.validate_on_submit():
#         Employee.update_info_employee(current_user.get_id(), form_for_employee.employee_fio.data,
#                                       form_for_employee.birthday.data, form_for_employee.mobile_phone_number.data,
#                                       form_for_employee.home_phone_number.data, form_for_employee.address.data)
#
#     return render_template('profile.html', employee=employer, form_for_employee=form_for_employee)
