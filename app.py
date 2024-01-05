from flask import Flask
from extensions import db, migrate, login_manager, ckeditor
from sqlalchemy.sql import text  # Import text for raw SQL execution

def create_app():
    """Application factory function"""
    app = Flask(__name__)

    # Configure the app for development with SQLite and a simple secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'dev'

    # Initialize extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    with app.app_context():
        # Import models here to avoid circular imports
        from models import User
        try:
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print('Connected to the database.')
        except Exception as e:
            print('Failed to connect to the database.')
            print(f'Exception: {e}')

        # Create all tables in the database which don't exist yet
        db.create_all()

    login_manager.login_view = 'auth.login'

    # Import and register blueprints
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
