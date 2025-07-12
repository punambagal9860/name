# import os
# from datetime import timedelta

# class Config:
#     """Base configuration class"""
#     # Database configuration
#     DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database/employees.db')
#     SQLALCHEMY_DATABASE_URI = DATABASE_URL
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ENGINE_OPTIONS = {
#         "pool_recycle": 300,
#         "pool_pre_ping": True,
#     }
    
#     # Security configuration
#     SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
#     SESSION_PERMANENT = False
#     PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
#     # Application configuration
#     DEBUG = True
#     TESTING = False
    
#     # Email configuration (for future features)
#     MAIL_SERVER = os.environ.get('MAIL_SERVER')
#     MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
#     MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
#     # Pagination
#     EMPLOYEES_PER_PAGE = 20
    
#     # Upload configuration
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
#     UPLOAD_FOLDER = 'uploads'
#     ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}

# class DevelopmentConfig(Config):
#     """Development configuration"""
#     DEBUG = True
#     SQLALCHEMY_ECHO = False  # Set to True for SQL debugging

# class ProductionConfig(Config):
#     """Production configuration"""
#     DEBUG = False
#     TESTING = False
    
#     # Override with secure production values
#     SECRET_KEY = os.environ.get('SESSION_SECRET')
#     DATABASE_URL = os.environ.get('DATABASE_URL')
    
#     # Production security settings
#     SESSION_COOKIE_SECURE = True
#     SESSION_COOKIE_HTTPONLY = True
#     SESSION_COOKIE_SAMESITE = 'Lax'

# class TestingConfig(Config):
#     """Testing configuration"""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
#     WTF_CSRF_ENABLED = False

# # Configuration dictionary
# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'testing': TestingConfig,
#     'default': DevelopmentConfig
# }
import os
from datetime import timedelta

# Get the base directory of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure the database directory exists
db_folder = os.path.join(basedir, 'database')
os.makedirs(db_folder, exist_ok=True)  # Create 'database/' if it doesn't exist

class Config:
    """Base configuration class"""
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(db_folder, 'employees.db'))
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Security configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # Application configuration
    DEBUG = True
    TESTING = False

    # Email configuration (for future features)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Pagination
    EMPLOYEES_PER_PAGE = 20

    # Upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # Override with secure production values
    SECRET_KEY = os.environ.get('SESSION_SECRET')
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
