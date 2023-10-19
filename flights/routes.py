from flights import app, db, bcrypt
from flask import render_template, request, session, redirect, url_for, flash, abort
from flights.forms import LoginForm, RegistrationForm, AdminLoginForm, AddFlightForm, UpdateFlightForm, SearchFlightForm
from flights.models import User, Flight, Seat, Booking
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/d')
# def dummy():
#     return render_template('dummy.html')


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


@app.route("/flight", methods=['GET', 'POST'])
@login_required
def flight():
    
    flights = Flight.query.all()

    return render_template('flight.html', flights=flights)


@app.route("/flight/add", methods=['GET', 'POST'])
@login_required
def add_flight():
    if current_user.email != 'admin':
        return redirect(url_for('home'))

    form = AddFlightForm()

    if form.validate_on_submit():
        Flight.add_flight(form)
        flash('Flight Added', 'success')

        return redirect(url_for('add_flight'))
    
    return render_template('add_flight.html', form=form)


@app.route("/flight/<int:flight_id>", methods=['GET', 'POST'])
@login_required
def book_seats(flight_id):

    flight = Flight.query.get_or_404(flight_id)

    if request.method == 'POST':

        seats = map(int, request.form.keys())
        seats = list(map(Seat.query.get_or_404, seats))

        for seat in seats:
            if seat.booked:
                flash('Sorry those tickets are booked my someone.', 'danger')
                return redirect(url_for('book_seats', flight_id=flight_id))

        for seat in seats:
            seat.book_seat(current_user.id)
        
        flash('Tickets booked.', 'success')
        return redirect(url_for('ticket'))

    return render_template('seats.html', flight=flight)

@app.route("/flight/<int:flight_id>/update", methods=['GET', 'POST'])
@login_required
def update_flight(flight_id):
    if current_user.email != 'admin':
        return redirect(url_for('home'))

    flight = Flight.query.get_or_404(flight_id)
    form = UpdateFlightForm()

    if form.validate_on_submit():
        flight.name = form.name.data
        flight.departure_date = form.departure_date.data
        flight.departure_time = form.departure_time.data
        flight.duration = form.duration.data
        flight.origin = form.origin.data
        flight.destination = form.destination.data
        db.session.commit()
        flash('Flight Updated', 'success')

        return redirect(url_for('flight'))
    
    elif request.method == 'GET':
        form.name.data = flight.name
        form.departure_date.data = flight.departure_date
        form.departure_time.data = flight.departure_time
        form.duration.data = flight.duration
        form.origin.data = flight.origin
        form.destination.data = flight.destination

    
    return render_template('update_flight.html', form=form)


@app.route("/flight/<int:flight_id>/cancel", methods=['POST'])
@login_required
def cancel_flight(flight_id):
    if current_user.email != 'admin':
        flash('Unautorized', 'warning')
        abort(403)

    ### send alerts
    
    cur_flight = Flight.query.get_or_404(flight_id)
    db.session.delete(cur_flight)
    db.session.commit()

    flash('Flight Canceled', 'success')
    
    return redirect(url_for('flight'))


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchFlightForm()

    if form.validate_on_submit():
        if form.validate_on_submit():
            flights = Flight.query.filter(Flight.avilable_seat != 0)
            
            if form.origin.data != 'None':
                flights = flights.filter(Flight.origin == form.origin.data)

            if form.destination.data != 'None':
                flights = flights.filter(Flight.destination == form.destination.data)

            if form.date.data:
                flights = flights.filter(Flight.departure_date >= form.date.data)

            flights = flights.all()
    else:
        flights = Flight.query.filter(Flight.avilable_seat != 0)
    
    flights = [flight.more_info() for flight in flights]
    return render_template('search.html', form=form, flights=flights)


@app.route("/ticket", methods=['GET', 'POST'])
@login_required
def ticket():
    if current_user.email == 'admin':
        tickets = Booking.query.all()
    else:
        tickets = Booking.query.filter(Booking.user_id==current_user.id).all()

    return render_template('ticket.html', tickets=tickets)


@app.route("/cancel/<int:ticket_id>/cancel", methods=['POST'])
@login_required
def cancel_ticket(ticket_id):
    
    tk = Booking.query.get_or_404(ticket_id)

    if current_user.email != 'admin' and current_user.id != tk.owner.id:
        abort(403)

    tk.cancel()

    flash('Ticket Canceled.', 'success')
    return redirect(url_for('ticket'))