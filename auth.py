from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import Usuario, ResenaPelicula
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import re
import requests
from forms.forms import FormularioRegistro, ResenaPeliculaForm


#!  Ruta para dar la bienvenida a usuarios no admin
#!--------------------------------------#
@app.route('/bienvenido')
def bienvenido():
    todas_resenas = ResenaPelicula.query.all()
    resenas = random.sample(todas_resenas, min(6, len(todas_resenas)))
    return render_template('bienvenido.html', resenas=resenas)
#!--------------------------------------#


#?--------------------------------------?#
#? Apartado de login y registro de un usuario
#?--------------------------------------?#


#! Ruta para el login
#!--------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        user = Usuario.query.filter_by(email=email).first()
        # Se utiliza check_password_hash para comparar el hash almacenado con la contraseña introducida
        if user and check_password_hash(user.contraseña, contraseña):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            if user.is_admin:
                return redirect(url_for('admin_menu'))
            else:
                return redirect(url_for('resenas'))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")
    return render_template('login.html')
#!--------------------------------------#


#! Ruta para registrar un nuevo usuario
#!--------------------------------------#
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellidos = form.apellidos.data
        telefono = form.telefono.data
        email = form.email.data
        contraseña = form.contraseña.data

        hashed_contraseña = generate_password_hash(contraseña, method='pbkdf2:sha256', salt_length=8)

        # Verificar si ya existe un usuario con este email
        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            flash("El usuario ya existe. Por favor, inicia sesión.", "warning")
            return redirect(url_for('login'))

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            email=email,
            contraseña=hashed_contraseña,
            is_admin=False
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
#!--------------------------------------#


#?--------------------------------------?#
#? Rutas para un usuario que esté logueado sin permisos de administrador
#?--------------------------------------?#


#! Ruta para ver las reseñas de un usuario
#!--------------------------------------#
@app.route('/resenas')
@login_required
def resenas():
    user_resenas = ResenaPelicula.query.filter_by(id_usuario=current_user.id).all()
    return render_template('reseñas.html', resenas=user_resenas)
#!--------------------------------------#


#! Ruta para borrar una reseña
#!--------------------------------------#
@app.route('/resena/delete/<int:review_id>', methods=['POST'])
@login_required
def eliminar_resena(review_id):
    resena = ResenaPelicula.query.get_or_404(review_id)
    db.session.delete(resena)
    db.session.commit()
    flash("Reseña borrada exitosamente", "success")
    return redirect(url_for('resenas'))
#!--------------------------------------#


# Función para obtener el póster (ver función de arriba)
def get_movie_poster(title):
    api_key = 'cddd798'  # Reemplaza con tu API key de OMDb
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get('Response') == 'True' and data.get('Poster') and data.get('Poster') != 'N/A':
        return data.get('Poster')
    else:
        return None
#!--------------------------------------#


#! Ruta para añadir una reseña
#!--------------------------------------#
def get_movie_poster(title):
    api_key = 'cddd798'  # Reemplaza con tu API key de OMDb
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    # Verifica que la respuesta sea exitosa y que exista un póster válido
    if data.get('Response') == 'True' and data.get('Poster') and data.get('Poster') != 'N/A':
        return data.get('Poster')
    else:
        return None


@app.route('/resena/add', methods=['GET', 'POST'])
@login_required
def nueva_resena():
    form = ResenaPeliculaForm()
    if form.validate_on_submit():
        titulo = form.titulo.data
        anio = form.anio.data
        duracion = form.duracion.data
        genero = form.genero.data
        puntuacion = form.puntuacion.data
        resena_texto = form.resena.data

        imagen_path = None
        # Buscar la URL del póster usando el título
        poster_url = get_movie_poster(titulo)
        if poster_url:
            response = requests.get(poster_url)
            if response.status_code == 200:
                # Definir la ruta de la carpeta donde se guardará la imagen: static/images
                image_dir = os.path.join(app.root_path, 'static', 'images')
                os.makedirs(image_dir, exist_ok=True)
                # Generar un nombre único para la imagen usando el título y un UUID
                filename = f"{titulo}_{uuid.uuid4().hex}.jpg"
                # Limpiar el nombre de archivo de caracteres no válidos
                filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
                image_full_path = os.path.join(image_dir, filename)
                with open(image_full_path, 'wb') as f:
                    f.write(response.content)
                # Guardar la ruta relativa, por ejemplo: images/archivo.jpg
                imagen_path = os.path.join('images', filename).replace('\\', '/')

        nueva_resena = ResenaPelicula(
            titulo=titulo,
            anio=anio,
            duracion=duracion,
            genero=genero,
            puntuacion=puntuacion,
            resena=resena_texto,
            imagen=imagen_path,  # Guarda la ruta de la imagen
            id_usuario=current_user.id
        )
        db.session.add(nueva_resena)
        db.session.commit()
        flash("Reseña añadida exitosamente", "success")
        return redirect(url_for('resenas'))
    return render_template('nueva_reseña.html', form=form)
#!--------------------------------------#


#! Ruta para editar una reseña
#!--------------------------------------#
@app.route('/resena/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def editar_resena(review_id):
    resena = ResenaPelicula.query.get_or_404(review_id)
    if resena.id_usuario != current_user.id:
        flash("No tienes permisos para editar esta reseña", "warning")
        return redirect(url_for('resenas'))
    
    if request.method == 'POST':
        resena.titulo = request.form.get('titulo')
        resena.anio = request.form.get('anio')
        resena.duracion = request.form.get('duracion')
        resena.genero = request.form.get('genero')
        resena.puntuacion = request.form.get('puntuacion')
        resena.resena = request.form.get('resena')
        db.session.commit()
        flash("Reseña actualizada exitosamente", "success")
        return redirect(url_for('resenas'))
    
    return render_template('editar_reseña.html', resena=resena)
#!--------------------------------------#


#! Ruta para el perfil de un usuario logueado
#!--------------------------------------#
@app.route('/perfil')
@login_required
def perfil():
    # Aquí puedes pasar el usuario actual a la plantilla
    return render_template('perfil.html', usuario=current_user)
#!--------------------------------------#


#! Ruta para editar un usuario que está logueado (método POST)
#!--------------------------------------#
@app.route('/perfil/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        user.nombre = request.form.get('nombre')
        user.apellidos = request.form.get('apellidos')
        user.telefono = request.form.get('telefono')
        # Obtener la contraseña del formulario
        new_password = request.form.get('contraseña')
        # Si se ha ingresado una nueva contraseña, la hasheamos
        if new_password:
            user.contraseña = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        db.session.commit()
        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for('perfil'))
    return render_template('edit_usuario.html', user=user)
#!--------------------------------------#


#! Ruta para borrar un usuario que está logueado (método POST)
#!--------------------------------------#
@app.route('/perfil/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuario borrado exitosamente", "success")
    return redirect(url_for('bienvenido'))
#!--------------------------------------#


#?--------------------------------------?#
#? Rutas para un usuario que esté logueado con permisos de administrador
#?--------------------------------------?#


#! Panel de administrador: muestra un menú para administrar usuarios y reseñas
#!--------------------------------------#
@app.route('/admin_menu')
@login_required
def admin_menu():
    if not current_user.is_admin:
        flash("No tienes permisos de administrador", "warning")
        return redirect(url_for('login'))
    users = Usuario.query.all()
    return render_template('admin_menu.html', users=users)
#!--------------------------------------#


#! Panel de administrador: muestra una tabla con todos los usuarios
#!--------------------------------------#
@app.route('/admin_usuarios')
@login_required
def admin_usuarios():
    if not current_user.is_admin:
        flash("No tienes permisos de administrador", "warning")
        return redirect(url_for('login'))
    users = Usuario.query.all()
    return render_template('admin_usuarios.html', users=users)
#!--------------------------------------#


#! Panel de administrador: muestra una tabla con todas las reseñas
#!--------------------------------------#
@app.route('/admin_reseñas')
@login_required
def admin_reseñas():
    if not current_user.is_admin:
        flash("No tienes permisos de administrador", "warning")
        return redirect(url_for('login'))
    # Realiza un JOIN entre ResenaPelicula y Usuario utilizando id_usuario
    reseñas_con_email = db.session.query(ResenaPelicula, Usuario.email).join(Usuario, ResenaPelicula.id_usuario == Usuario.id).all()
    return render_template('admin_reseñas.html', reseñas=reseñas_con_email)
#!--------------------------------------#


#! Ruta para editar una reseña
#!--------------------------------------#
@app.route('/admin_reseñas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reseña(id):
    if not current_user.is_admin:
        flash("No tienes permisos para realizar esta acción", "warning")
        return redirect(url_for('login'))
    reseña = ResenaPelicula.query.get_or_404(id)
    if request.method == 'POST':
        reseña.titulo = request.form.get('titulo')
        reseña.anio = request.form.get('anio')
        reseña.duracion = request.form.get('duracion')
        reseña.genero = request.form.get('genero')
        reseña.puntuacion = request.form.get('puntuacion')
        reseña.resena = request.form.get('resena')
        db.session.commit()
        flash("Reseña actualizada exitosamente", "success")
        return redirect(url_for('admin_reseñas'))
    return render_template('admin_edit_reseña.html', reseña=reseña)
#!--------------------------------------#


#! Ruta para borrar una reseña (método POST)
#!--------------------------------------#
@app.route('/admin_reseñas/delete/<int:id>', methods=['POST'])
@login_required
def delete_reseña(id):
    if not current_user.is_admin:
        flash("No tienes permisos para realizar esta acción", "warning")
        return redirect(url_for('login'))
    reseña = ResenaPelicula.query.get_or_404(id)
    db.session.delete(reseña)
    db.session.commit()
    flash("Reseña borrada exitosamente", "success")
    return redirect(url_for('admin_reseñas'))
#!--------------------------------------#


#! Ruta para añadir un usuario
#!--------------------------------------#
@app.route('/admin_usuarios/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash("No tienes permisos para realizar esta acción", "warning")
        return redirect(url_for('login'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        hashed_contraseña = generate_password_hash(contraseña, method='pbkdf2:sha256', salt_length=8)
        # Aquí estamos creando un usuario normal (is_admin=False)
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            email=email,
            contraseña=hashed_contraseña,
            is_admin=False
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario añadido exitosamente", "success")
        return redirect(url_for('admin_usuarios'))
    return render_template('add_user.html')
#!--------------------------------------#


#! Ruta para editar un usuario
#!--------------------------------------#
@app.route('/admin_usuarios/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_users(user_id):
    if not current_user.is_admin:
        flash("No tienes permisos para realizar esta acción", "warning")
        return redirect(url_for('login'))
    user = Usuario.query.get_or_404(user_id)
    if request.method == 'POST':
        user.nombre = request.form.get('nombre')
        user.apellidos = request.form.get('apellidos')
        user.telefono = request.form.get('telefono')
        # Obtener la nueva contraseña del formulario
        new_password = request.form.get('contraseña')
        # Solo actualizamos la contraseña si se ha proporcionado un valor nuevo
        if new_password:
            user.contraseña = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        db.session.commit()
        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for('admin_usuarios'))
    return render_template('edit_usuarios.html', user=user)
#!--------------------------------------#


#! Ruta para borrar un usuario (método POST)
#!--------------------------------------#
@app.route('/admin_usuarios/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_users(user_id):
    if not current_user.is_admin:
        flash("No tienes permisos para realizar esta acción", "warning")
        return redirect(url_for('login'))
    user = Usuario.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuario borrado exitosamente", "success")
    return redirect(url_for('admin_usuarios'))
#!--------------------------------------#


#?--------------------------------------?#
#? Ruta para cerrar sesión
#?--------------------------------------?#


#! Ruta para cerrar sesión
#!--------------------------------------#
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "info")
    return redirect(url_for('bienvenido'))
#!--------------------------------------#



