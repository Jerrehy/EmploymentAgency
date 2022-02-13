class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'uiezfrusneudzn'
    password = '9506ead55c0f930839988a21ffac242203b044a97e18f18f0b20e9f8c84c9f90'
    host = 'ec2-34-249-49-9.eu-west-1.compute.amazonaws.com'
    db_name = 'deau5afe7llnqc'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '21epkpo3ksa8e2sal12poe'
