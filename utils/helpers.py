from functools import wraps
from flask import session, redirect, url_for, flash
import re
from datetime import datetime
import csv
import io

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        if session.get('admin_role') != 'Admin':
            flash('Admin access required', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    # Check for at least one letter and one number
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def validate_username(username):
    """Validate username format"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    if not re.match(pattern, username):
        return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores"
    return True, "Username is valid"

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_date(date_obj):
    """Format date object to string"""
    if date_obj:
        return date_obj.strftime('%Y-%m-%d')
    return ''

def format_datetime(datetime_obj):
    """Format datetime object to string"""
    if datetime_obj:
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return ''

def parse_date(date_string):
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None

def generate_csv_response(data, filename, headers):
    """Generate CSV response from data"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(headers)
    
    # Write data
    for row in data:
        writer.writerow(row)
    
    output.seek(0)
    return output.getvalue()

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_safe_filename(filename):
    """Generate safe filename"""
    import unicodedata
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    filename = re.sub(r'[^\w\s-]', '', filename).strip()
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename

def paginate_query(query, page, per_page):
    """Paginate a SQLAlchemy query"""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page * per_page < total else None
    }

def get_employee_stats(employees):
    """Calculate employee statistics"""
    if not employees:
        return {
            'total': 0,
            'avg_salary': 0,
            'departments': {},
            'roles': {},
            'salary_ranges': {}
        }
    
    total = len(employees)
    avg_salary = sum(emp.salary for emp in employees) / total
    
    # Department distribution
    departments = {}
    for emp in employees:
        departments[emp.department] = departments.get(emp.department, 0) + 1
    
    # Role distribution
    roles = {}
    for emp in employees:
        roles[emp.role] = roles.get(emp.role, 0) + 1
    
    # Salary ranges
    salary_ranges = {
        'Under $30k': 0,
        '$30k - $50k': 0,
        '$50k - $75k': 0,
        '$75k - $100k': 0,
        'Over $100k': 0
    }
    
    for emp in employees:
        salary = emp.salary
        if salary < 30000:
            salary_ranges['Under $30k'] += 1
        elif salary < 50000:
            salary_ranges['$30k - $50k'] += 1
        elif salary < 75000:
            salary_ranges['$50k - $75k'] += 1
        elif salary < 100000:
            salary_ranges['$75k - $100k'] += 1
        else:
            salary_ranges['Over $100k'] += 1
    
    return {
        'total': total,
        'avg_salary': avg_salary,
        'departments': departments,
        'roles': roles,
        'salary_ranges': salary_ranges
    }

def log_user_activity(user_id, action, details=None):
    """Log user activity (for future audit trail)"""
    # This could be expanded to write to a log file or database
    import logging
    logging.info(f"User {user_id} performed action: {action}. Details: {details}")

def sanitize_search_term(term):
    """Sanitize search term for safe database queries"""
    if not term:
        return ''
    
    # Remove special characters that could cause issues
    term = re.sub(r'[^\w\s-]', '', term)
    term = term.strip()
    
    return term

def get_breadcrumbs(current_page, **kwargs):
    """Generate breadcrumbs for navigation"""
    breadcrumbs = [
        {'name': 'Dashboard', 'url': url_for('index')}
    ]
    
    if current_page == 'employees':
        breadcrumbs.append({'name': 'Employees', 'url': url_for('employees')})
    elif current_page == 'add_employee':
        breadcrumbs.extend([
            {'name': 'Employees', 'url': url_for('employees')},
            {'name': 'Add Employee', 'url': None}
        ])
    elif current_page == 'edit_employee':
        breadcrumbs.extend([
            {'name': 'Employees', 'url': url_for('employees')},
            {'name': f'Edit {kwargs.get("employee_name", "Employee")}', 'url': None}
        ])
    elif current_page == 'reports':
        breadcrumbs.append({'name': 'Reports', 'url': url_for('reports')})
    elif current_page == 'profile':
        breadcrumbs.append({'name': 'Profile', 'url': None})
    
    return breadcrumbs