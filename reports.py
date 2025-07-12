from flask import render_template, request, make_response, session, redirect, url_for, flash
from app import app, db
from models import Employee
import csv
import io
import logging
from datetime import datetime

@app.route('/reports')
def reports():
    """Reports dashboard"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get summary statistics
        total_employees = Employee.query.count()
        
        # Department-wise statistics
        dept_stats = db.session.query(
            Employee.department,
            db.func.count(Employee.id).label('count'),
            db.func.avg(Employee.salary).label('avg_salary'),
            db.func.min(Employee.salary).label('min_salary'),
            db.func.max(Employee.salary).label('max_salary')
        ).group_by(Employee.department).all()
        
        # Role-wise statistics
        role_stats = db.session.query(
            Employee.role,
            db.func.count(Employee.id).label('count'),
            db.func.avg(Employee.salary).label('avg_salary')
        ).group_by(Employee.role).all()
        
        # Salary range distribution
        salary_ranges = [
            ('< 30,000', Employee.query.filter(Employee.salary < 30000).count()),
            ('30,000 - 50,000', Employee.query.filter(Employee.salary.between(30000, 50000)).count()),
            ('50,000 - 75,000', Employee.query.filter(Employee.salary.between(50000, 75000)).count()),
            ('75,000 - 100,000', Employee.query.filter(Employee.salary.between(75000, 100000)).count()),
            ('> 100,000', Employee.query.filter(Employee.salary > 100000).count())
        ]
        
        return render_template('reports.html',
                             total_employees=total_employees,
                             dept_stats=dept_stats,
                             role_stats=role_stats,
                             salary_ranges=salary_ranges)
        
    except Exception as e:
        logging.error(f"Error generating reports: {str(e)}")
        flash('Error loading reports', 'error')
        return render_template('reports.html',
                             total_employees=0,
                             dept_stats=[],
                             role_stats=[],
                             salary_ranges=[])

@app.route('/export_csv')
def export_csv():
    """Export employees to CSV"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get filter parameters
        department = request.args.get('department', '')
        min_salary = request.args.get('min_salary', type=float)
        max_salary = request.args.get('max_salary', type=float)
        
        # Build query
        query = Employee.query
        
        if department:
            query = query.filter(Employee.department == department)
        if min_salary is not None:
            query = query.filter(Employee.salary >= min_salary)
        if max_salary is not None:
            query = query.filter(Employee.salary <= max_salary)
        
        employees = query.order_by(Employee.name).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Name', 'Department', 'Role', 'Salary', 'Date of Joining', 'Created At'])
        
        # Write employee data
        for emp in employees:
            writer.writerow([
                emp.id,
                emp.name,
                emp.department,
                emp.role,
                emp.salary,
                emp.date_of_joining.strftime('%Y-%m-%d'),
                emp.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Prepare response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=employees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        logging.error(f"Error exporting CSV: {str(e)}")
        flash('Error exporting data', 'error')
        return redirect(url_for('reports'))

@app.route('/export_department_csv/<department>')
def export_department_csv(department):
    """Export specific department employees to CSV"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        employees = Employee.query.filter_by(department=department).order_by(Employee.name).all()
        
        if not employees:
            flash(f'No employees found in {department} department', 'warning')
            return redirect(url_for('reports'))
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Name', 'Role', 'Salary', 'Date of Joining'])
        
        # Write employee data
        for emp in employees:
            writer.writerow([
                emp.id,
                emp.name,
                emp.role,
                emp.salary,
                emp.date_of_joining.strftime('%Y-%m-%d')
            ])
        
        # Prepare response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={department}_employees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        logging.error(f"Error exporting department CSV: {str(e)}")
        flash('Error exporting data', 'error')
        return redirect(url_for('reports'))
