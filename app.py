from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a la página de login si no está autenticado

from models import Usuario, ResenaPelicula
import random

@app.route('/')
def home():
    todas_resenas = ResenaPelicula.query.all()
    resenas = random.sample(todas_resenas, min(6, len(todas_resenas)))
    return render_template('bienvenido.html', resenas=resenas)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

