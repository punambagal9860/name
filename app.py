import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///employees.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    import auth
    import reports
    
    # Create all tables
    db.create_all()
    
    # Create default admin user if not exists
    from models import Admin
    from werkzeug.security import generate_password_hash
    
    try:
        # Check if admin user exists
        admin_exists = Admin.query.filter_by(username='admin').first()
        if not admin_exists:
            admin = Admin(
                username='admin',
                email='admin@company.com',
                password_hash=generate_password_hash('admin123'),
                role='Admin'
            )
            db.session.add(admin)
            db.session.commit()
            logging.info("Default admin user created: admin/admin123")
    except Exception as e:
        logging.error(f"Error creating default admin user: {str(e)}")
        # If there's an error, it might be due to missing columns
        # Let's try to migrate by dropping and recreating the table
        try:
            db.drop_all()
            db.create_all()
            admin = Admin(
                username='admin',
                email='admin@company.com',
                password_hash=generate_password_hash('admin123'),
                role='Admin'
            )
            db.session.add(admin)
            db.session.commit()
            logging.info("Database migrated and default admin user created: admin/admin123")
        except Exception as e2:
            logging.error(f"Database migration failed: {str(e2)}")
