class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'postgres'
    password = 'Qwerty7'
    host = 'localhost'
    db_name = 'employment_agency'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '21epkpo3ksa8e2sal12poe'
