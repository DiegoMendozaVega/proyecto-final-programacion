from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length

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
