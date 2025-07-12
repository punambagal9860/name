from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import app, db
from models import Admin
import logging

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Username and password are required', 'error')
                return render_template('login.html')
            
            # Find admin user
            admin = Admin.query.filter_by(username=username).first()
            
            if admin and check_password_hash(admin.password_hash, password):
                session['admin_id'] = admin.id
                session['admin_username'] = admin.username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')
                
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
            return render_template('login.html')
    
    # If already logged in, redirect to dashboard
    if 'admin_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.context_processor
def inject_user():
    """Inject admin user info into all templates"""
    if 'admin_id' in session:
        return dict(
            current_admin=session.get('admin_username'),
            is_logged_in=True
        )
    return dict(current_admin=None, is_logged_in=False)
