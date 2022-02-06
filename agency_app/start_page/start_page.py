from flask import Blueprint, render_template

start = Blueprint('start', __name__, template_folder="templates")


# Начальная страница сайта
@start.route('/')
@start.route('/main', methods=['GET'])
def begin_page():
    return render_template('start/main.html')
