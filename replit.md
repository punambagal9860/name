# Employee Management System

## Overview

This is a Flask-based web application for managing employee records. It provides a comprehensive CRUD (Create, Read, Update, Delete) interface for employee data with authentication, reporting capabilities, and data export functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**2025-07-12**: Enhanced authentication system with user registration, email login, and profile management features.

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

### Authentication (`auth.py`)
- Session-based login/logout system with email or username login
- User registration with email validation and role assignment
- Profile management with password change functionality
- Default admin user creation (username: admin, password: admin123, email: admin@company.com)
- Route protection middleware
- Enhanced user session management with role-based access

### Main Routes (`routes.py`)
- Dashboard with employee statistics and recent additions
- Employee listing with search and filter capabilities
- CRUD operations for employee management

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
├── models.py           # Database models
├── routes.py           # Main application routes
├── auth.py             # Authentication routes
├── reports.py          # Reporting and analytics
├── templates/          # HTML templates
│   ├── base.html       # Base template with enhanced navigation
│   ├── index.html      # Dashboard
│   ├── employees.html  # Employee listing
│   ├── add_employee.html    # Employee creation form
│   ├── edit_employee.html   # Employee editing form
│   ├── login.html      # Login page with registration link
│   ├── register.html   # User registration form
│   ├── profile.html    # User profile management
│   └── reports.html    # Reports dashboard
└── static/             # Static assets
    ├── css/custom.css  # Custom styling
    └── js/main.js      # JavaScript functionality
```

The application follows a traditional MVC pattern with clear separation of concerns, making it easy to maintain and extend.