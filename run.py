from app import app
import auth  # Aseguramos que se carguen las rutas de autenticación

if __name__ == '__main__':
    app.run(debug=True)