from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class ResenaPelicula(db.Model):
    __tablename__ = 'resenas_peliculas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    anio = db.Column(db.Integer)
    duracion = db.Column(db.Integer)
    genero = db.Column(db.String(100))
    puntuacion = db.Column(db.Numeric(3, 1))
    resena = db.Column(db.Text)
    imagen = db.Column(db.String(255))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))