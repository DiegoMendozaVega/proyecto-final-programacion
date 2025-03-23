from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, Regexp, Length, NumberRange

class FormularioRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=15)])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Introduce un email válido."),
        Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|es)$', 
               message="El email debe contener una extensión válida (.com o .es).")
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres."),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).+$',
               message="La contraseña debe contener al menos una letra, un número y un carácter especial.")
    ])
    submit = SubmitField('Registrarse')


class ResenaPeliculaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=1, max=100)])
    anio = IntegerField('Año', validators=[
        DataRequired(),
        NumberRange(min=1888, message="Ingrese un año válido")  # El cine se inició en 1888
    ])
    duracion = IntegerField('Duración', validators=[
        DataRequired(),
        NumberRange(min=1, message="La duración debe ser mayor a 0")
    ])
    genero = StringField('Género', validators=[DataRequired(), Length(min=2, max=50)])
    puntuacion = DecimalField('Puntuación', validators=[
        DataRequired(),
        NumberRange(min=0, max=5, message="La puntuación debe estar entre 0 y 5")
    ])
    resena = TextAreaField('Reseña', validators=[DataRequired(), Length(min=10, message="La reseña debe tener al menos 10 caracteres")])
    submit = SubmitField('Publicar Reseña')

