from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import Employee
from datetime import datetime
import logging

@app.route('/')
def index():
    """Dashboard showing employee statistics"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        total_employees = Employee.query.count()
        departments = db.session.query(Employee.department).distinct().count()
        avg_salary = db.session.query(db.func.avg(Employee.salary)).scalar() or 0
        
        # Recent employees (last 5)
        recent_employees = Employee.query.order_by(Employee.created_at.desc()).limit(5).all()
        
        # Department-wise count
        dept_stats = db.session.query(
            Employee.department,
            db.func.count(Employee.id).label('count')
        ).group_by(Employee.department).all()
        
        return render_template('index.html',
                             total_employees=total_employees,
                             departments=departments,
                             avg_salary=avg_salary,
                             recent_employees=recent_employees,
                             dept_stats=dept_stats)
    except Exception as e:
        logging.error(f"Error in dashboard: {str(e)}")
        flash('Error loading dashboard data', 'error')
        return render_template('index.html',
                             total_employees=0,
                             departments=0,
                             avg_salary=0,
                             recent_employees=[],
                             dept_stats=[])

@app.route('/employees')
def employees():
    """View all employees with search and filter"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get search and filter parameters
        search = request.args.get('search', '')
        department = request.args.get('department', '')
        min_salary = request.args.get('min_salary', type=float)
        max_salary = request.args.get('max_salary', type=float)
        
        # Build query
        query = Employee.query
        
        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    Employee.name.contains(search),
                    Employee.role.contains(search),
                    Employee.department.contains(search)
                )
            )
        
        # Apply department filter
        if department:
            query = query.filter(Employee.department == department)
        
        # Apply salary range filter
        if min_salary is not None:
            query = query.filter(Employee.salary >= min_salary)
        if max_salary is not None:
            query = query.filter(Employee.salary <= max_salary)
        
        # Execute query
        employees_list = query.order_by(Employee.name).all()
        
        # Get all departments for filter dropdown
        departments = db.session.query(Employee.department).distinct().all()
        departments = [dept[0] for dept in departments]
        
        return render_template('employees.html',
                             employees=employees_list,
                             departments=departments,
                             search=search,
                             selected_department=department,
                             min_salary=min_salary,
                             max_salary=max_salary)
    except Exception as e:
        logging.error(f"Error fetching employees: {str(e)}")
        flash('Error loading employees', 'error')
        return render_template('employees.html',
                             employees=[],
                             departments=[])

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    """Add new employee"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            salary = request.form.get('salary', type=float)
            role = request.form.get('role', '').strip()
            date_of_joining = request.form.get('date_of_joining')
            
            # Validate required fields
            if not all([name, department, salary, role, date_of_joining]):
                flash('All fields are required', 'error')
                return render_template('add_employee.html')
            
            # Validate salary
            if salary <= 0:
                flash('Salary must be greater than 0', 'error')
                return render_template('add_employee.html')
            
            # Parse date
            try:
                joining_date = datetime.strptime(date_of_joining, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('add_employee.html')
            
            # Create new employee
            employee = Employee(
                name=name,
                department=department,
                salary=salary,
                role=role,
                date_of_joining=joining_date
            )
            
            db.session.add(employee)
            db.session.commit()
            
            flash(f'Employee {name} added successfully!', 'success')
            return redirect(url_for('employees'))
            
        except Exception as e:
            logging.error(f"Error adding employee: {str(e)}")
            db.session.rollback()
            flash('Error adding employee', 'error')
            return render_template('add_employee.html')
    
    return render_template('add_employee.html')

@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Edit employee details"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            salary = request.form.get('salary', type=float)
            role = request.form.get('role', '').strip()
            date_of_joining = request.form.get('date_of_joining')
            
            # Validate required fields
            if not all([name, department, salary, role, date_of_joining]):
                flash('All fields are required', 'error')
                return render_template('edit_employee.html', employee=employee)
            
            # Validate salary
            if salary <= 0:
                flash('Salary must be greater than 0', 'error')
                return render_template('edit_employee.html', employee=employee)
            
            # Parse date
            try:
                joining_date = datetime.strptime(date_of_joining, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('edit_employee.html', employee=employee)
            
            # Update employee
            employee.name = name
            employee.department = department
            employee.salary = salary
            employee.role = role
            employee.date_of_joining = joining_date
            employee.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'Employee {name} updated successfully!', 'success')
            return redirect(url_for('employees'))
        
        return render_template('edit_employee.html', employee=employee)
        
    except Exception as e:
        logging.error(f"Error editing employee: {str(e)}")
        db.session.rollback()
        flash('Error updating employee', 'error')
        return redirect(url_for('employees'))

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    """Delete employee"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        employee = Employee.query.get_or_404(employee_id)
        name = employee.name
        
        db.session.delete(employee)
        db.session.commit()
        
        flash(f'Employee {name} deleted successfully!', 'success')
        
    except Exception as e:
        logging.error(f"Error deleting employee: {str(e)}")
        db.session.rollback()
        flash('Error deleting employee', 'error')
    
    return redirect(url_for('employees'))

# API Routes
@app.route('/api/employees')
def api_employees():
    """API endpoint to get all employees"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        employees = Employee.query.all()
        return jsonify([emp.to_dict() for emp in employees])
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/employees/<int:employee_id>')
def api_employee(employee_id):
    """API endpoint to get specific employee"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        employee = Employee.query.get_or_404(employee_id)
        return jsonify(employee.to_dict())
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return jsonify({'error': 'Employee not found'}), 404