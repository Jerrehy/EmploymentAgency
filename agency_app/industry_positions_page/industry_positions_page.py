from flask import render_template, Blueprint
from agency_app.models import JobPosition, Industry


# Создание узла связанного с должностями и отраслями
industry_positions = Blueprint('industry_positions', __name__, template_folder="templates")


# Просмотр всех доступных должностей и отраслей
@industry_positions.route('/all_industry_positions', methods=['GET', 'POST'])
def industry_positions_view():
    # Вывод всех должностей
    all_job_positions = JobPosition.get_all_job_positions()
    # Вывод всех отраслей
    all_industries = Industry.get_all_industry()

    return render_template('industry_positions/all_industry_positions.html', all_job_positions=all_job_positions,
                           all_industries=all_industries)
