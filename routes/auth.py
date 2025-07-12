from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import Admin
import logging
import re
from datetime import datetime

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
            
            # Find admin user by username or email
            admin = Admin.query.filter(
                db.or_(Admin.username == username, Admin.email == username)
            ).first()
            
            if admin and admin.is_active and check_password_hash(admin.password_hash, password):
                # Update last login time
                admin.last_login = datetime.utcnow()
                db.session.commit()
                
                session['admin_id'] = admin.id
                session['admin_username'] = admin.username
                session['admin_email'] = admin.email
                session['admin_role'] = admin.role
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                if admin and not admin.is_active:
                    flash('Account is inactive. Please contact administrator.', 'error')
                else:
                    flash('Invalid username/email or password', 'error')
                return render_template('login.html')
                
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
            return render_template('login.html')
    
    # If already logged in, redirect to dashboard
    if 'admin_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            role = request.form.get('role', 'HR').strip()
            
            # Validate required fields
            if not all([username, email, password, confirm_password]):
                flash('All fields are required', 'error')
                return render_template('register.html')
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                flash('Please enter a valid email address', 'error')
                return render_template('register.html')
            
            # Validate password strength
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return render_template('register.html')
            
            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('register.html')
            
            # Check if username already exists
            if Admin.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return render_template('register.html')
            
            # Check if email already exists
            if Admin.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
                return render_template('register.html')
            
            # Validate role
            if role not in ['Admin', 'HR']:
                role = 'HR'
            
            # Create new user
            new_admin = Admin(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role=role
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile management"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    try:
        admin = Admin.query.get_or_404(session['admin_id'])
        
        if request.method == 'POST':
            # Get form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validate required fields
            if not username or not email:
                flash('Username and email are required', 'error')
                return render_template('profile.html', admin=admin)
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                flash('Please enter a valid email address', 'error')
                return render_template('profile.html', admin=admin)
            
            # Check if username already exists (excluding current user)
            existing_user = Admin.query.filter(
                Admin.username == username,
                Admin.id != admin.id
            ).first()
            if existing_user:
                flash('Username already exists', 'error')
                return render_template('profile.html', admin=admin)
            
            # Check if email already exists (excluding current user)
            existing_email = Admin.query.filter(
                Admin.email == email,
                Admin.id != admin.id
            ).first()
            if existing_email:
                flash('Email already exists', 'error')
                return render_template('profile.html', admin=admin)
            
            # Update basic info
            admin.username = username
            admin.email = email
            
            # Handle password change
            if new_password:
                if not current_password:
                    flash('Current password is required to change password', 'error')
                    return render_template('profile.html', admin=admin)
                
                if not check_password_hash(admin.password_hash, current_password):
                    flash('Current password is incorrect', 'error')
                    return render_template('profile.html', admin=admin)
                
                if len(new_password) < 6:
                    flash('New password must be at least 6 characters long', 'error')
                    return render_template('profile.html', admin=admin)
                
                if new_password != confirm_password:
                    flash('New passwords do not match', 'error')
                    return render_template('profile.html', admin=admin)
                
                admin.password_hash = generate_password_hash(new_password)
            
            db.session.commit()
            
            # Update session data
            session['admin_username'] = admin.username
            session['admin_email'] = admin.email
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        
        return render_template('profile.html', admin=admin)
        
    except Exception as e:
        logging.error(f"Profile error: {str(e)}")
        db.session.rollback()
        flash('Error updating profile', 'error')
        return redirect(url_for('index'))

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
            current_email=session.get('admin_email'),
            current_role=session.get('admin_role'),
            is_logged_in=True
        )
    return dict(
        current_admin=None, 
        current_email=None,
        current_role=None,
        is_logged_in=False
    )