# Employee Management System

## Overview

This is a Flask-based web application for managing employee records. It provides a comprehensive CRUD (Create, Read, Update, Delete) interface for employee data with authentication, reporting capabilities, and data export functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**2025-07-12**: 
- Enhanced authentication system with user registration, email login, and profile management features
- Reorganized project structure with separate modules for routes, utilities, and configuration
- Added comprehensive configuration management with environment-specific settings
- Created utility helpers for common operations and validations

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: SQLite (default) with support for PostgreSQL via DATABASE_URL environment variable
- **Authentication**: Session-based authentication with password hashing using Werkzeug
- **Application Structure**: Modular design with separate files for routes, models, authentication, and reports

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme
- **CSS Framework**: Bootstrap 5 with Font Awesome icons
- **JavaScript**: Vanilla JavaScript for form validation and UI interactions
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

## Key Components

### Models (`models.py`)
- **Employee Model**: Core entity with fields for name, department, role, salary, date of joining, and audit timestamps
- **Admin Model**: Enhanced user authentication with username, email, password hash, role (Admin/HR), active status, and last login tracking

### Authentication (`routes/auth.py`)
- Session-based login/logout system with email or username login
- User registration with email validation and role assignment
- Profile management with password change functionality
- Default admin user creation (username: admin, password: admin123, email: admin@company.com)
- Route protection middleware
- Enhanced user session management with role-based access

### Employee Management (`routes/employee.py`)
- Dashboard with employee statistics and visualizations
- Employee CRUD operations with comprehensive validation
- Search and filter functionality with multiple parameters
- API endpoints for employee data access
- Export functionality for data analysis

### Configuration (`config.py`)
- Environment-specific configuration classes
- Database connection settings and security parameters
- Email configuration for future features
- Application settings with secure defaults

### Utilities (`utils/helpers.py`)
- Authentication decorators (login_required, admin_required)
- Form validation functions for email, password, and username
- Data formatting utilities (currency, date, datetime)
- CSV generation and file handling functions
- Statistical analysis helpers for employee data

### Reports (`reports.py`)
- Statistical analysis by department and role
- Salary distribution reports
- CSV export functionality

### Database Configuration
- SQLite for development (employees.db)
- PostgreSQL support via DATABASE_URL environment variable
- Connection pooling with health checks enabled

## Data Flow

1. **Authentication Flow**: Users login through `/login` route, session stored, redirected to dashboard
2. **Employee Management**: CRUD operations through dedicated routes with form validation
3. **Reporting**: Database queries aggregate employee data for statistics and insights
4. **Export**: CSV generation from database records for external use

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Werkzeug: Password hashing and security utilities

### Frontend Libraries
- Bootstrap 5: UI framework with dark theme
- Font Awesome 6: Icon library
- Custom CSS for additional styling

## Deployment Strategy

### Environment Configuration
- `SESSION_SECRET`: Session encryption key (defaults to development key)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- Debug mode enabled for development

### Production Considerations
- ProxyFix middleware configured for reverse proxy deployment
- Database connection pooling configured
- Logging configured for debugging
- Session management with secure defaults needed for production

### File Structure
```
├── app.py              # Application factory and configuration
├── main.py             # Application entry point
├── config.py           # Configuration management
├── models.py           # Database models
├── reports.py          # Reporting and analytics
├── routes/             # Route modules
│   ├── __init__.py     # Package initialization
│   ├── auth.py         # Authentication routes
│   └── employee.py     # Employee management routes
├── utils/              # Utility functions
│   ├── __init__.py     # Package initialization
│   └── helpers.py      # Helper functions and decorators
├── templates/          # HTML templates
│   ├── base.html       # Base template with enhanced navigation
│   ├── index.html      # Dashboard
│   ├── dashboard.html  # Alternative dashboard view
│   ├── employees.html  # Employee listing
│   ├── view_employees.html # Alternative employee view
│   ├── add_employee.html    # Employee creation form
│   ├── edit_employee.html   # Employee editing form
│   ├── login.html      # Login page with registration link
│   ├── register.html   # User registration form
│   ├── signup.html     # Alternative signup page
│   ├── profile.html    # User profile management
│   └── reports.html    # Reports dashboard
├── static/             # Static assets
│   ├── css/custom.css  # Custom styling
│   └── js/main.js      # JavaScript functionality
└── database/           # Database files
    └── employees.db    # SQLite database (development)
```

The application follows a traditional MVC pattern with clear separation of concerns, making it easy to maintain and extend.