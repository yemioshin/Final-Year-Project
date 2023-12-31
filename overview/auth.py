from flask import Blueprint, render_template, request, flash,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', 'danger')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', 'danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', 'danger')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', 'danger')
        else:
            # Check if the email already exists in the database
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email address already exists. Please log in or use another email address.', 'danger')
                return redirect(url_for('auth.register'))
            
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username address already exists. Please log in or use another username.', 'danger')
                return redirect(url_for('auth.register'))

            # Create a new user
            new_user = User(email=email, first_name=first_name, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', 'success')
            return redirect(url_for('views.home'))
            # add user to database
            

    return render_template("auth/register.html", user=current_user)