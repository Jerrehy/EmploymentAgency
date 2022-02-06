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

