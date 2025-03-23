from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Conexión a la base de datos SQLite
engine = create_engine("sqlite:///db.sqlite3", echo=True)
Base = declarative_base()

# Definición de la tabla de usuarios (asegúrate de que ya exista en tu proyecto)
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    # Otros campos de la tabla usuarios

# Definición de la tabla de reseñas de películas
class ResenaPelicula(Base):
    __tablename__ = 'resenas_peliculas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    anio = Column(Integer)
    duracion = Column(Integer)
    genero = Column(String(100))
    puntuacion = Column(Numeric(3, 1))
    resena = Column(Text)
    imagen = Column(String(255))
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    
    # Relación con la tabla de usuarios
    usuario = relationship("Usuario", backref="resenas")

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Ejemplo de cómo trabajar con una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Aquí podrías añadir lógica para insertar, consultar, actualizar, etc.
