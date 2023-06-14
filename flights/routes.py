from flights import app, db, bcrypt
from flask import render_template, request, session, redirect, url_for, flash
from flights.forms import LoginForm, RegistrationForm, AdminLoginForm, AddFlightForm
from flights.models import User, Flight, Seat, Booking
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! log in please', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, False)
            next_page = request.args.get('next')
            flash('Login Successful.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if current_user.is_authenticated:
        flash('Logout first !', 'info')
        return redirect(url_for('home'))
    
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.name.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, False)
            flash('Login as Admin.', 'success')
            return redirect(url_for('home'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('admin-login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('logout Successful', 'success')
    return redirect(url_for('home'))


@app.route("/flight/add", methods=['GET', 'POST'])
@login_required
def add_flight():
    if current_user.email != 'admin':
        return redirect(url_for('home'))

    form = AddFlightForm()
    print(form)

    if form.validate_on_submit():
        Flight.add_flight(form)
        flash('Flight Added', 'success')

        return redirect(url_for('add_flight'))
    
    return render_template('add_flight.html', form=form)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    return render_template('search.html')


@app.route("/ticket", methods=['GET', 'POST'])
@login_required
def ticket():
    return render_template('ticket.html')