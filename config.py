import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'mi_clave_secreta'  # Fundamental para la gestión de sesiones

