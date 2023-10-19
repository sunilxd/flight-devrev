from flights import db, login_manager
from flask_login import UserMixin
import datetime as dt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class dummy():
    pass

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    tickets = db.relationship('Booking', backref='owner', lazy=True)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Flight(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    min_price = db.Column(db.Integer, nullable=False)
    avilable_seat = db.Column(db.Integer, nullable=False)

    seats = db.relationship('Seat', backref='flight', lazy=True, cascade='all, delete')

    def add_flight(form):

        new_flight = Flight(
            name=form.name.data,
            departure_date=form.departure_date.data,
            departure_time=form.departure_time.data,
            duration=form.duration.data,
            origin=form.origin.data,
            destination=form.destination.data,
            min_price=min(form.economy_price.data, form.business_price.data, form.firstclass_price.data),
            avilable_seat=form.economy_seat.data+form.business_seat.data+form.firstclass_seat.data,

        )
        db.session.add(new_flight)
        db.session.commit()
        db.session.refresh(new_flight)

        prev = 1

        price = form.economy_price.data
        cur = form.economy_seat.data
        for i in range(prev, cur+prev):
            db.session.add(Seat(flight_id=new_flight.id, name='Economy', number=i, price=price))
        prev += cur

        price = form.business_price.data
        cur = form.business_seat.data
        for i in range(prev, cur+prev):
            db.session.add(Seat(flight_id=new_flight.id, name='Business', number=i, price=price))
        prev += cur

        price = form.firstclass_price.data
        cur = form.firstclass_seat.data
        for i in range(prev, cur+prev):
            db.session.add(Seat(flight_id=new_flight.id, name='First Class', number=i, price=price))
        prev += cur


        db.session.commit()

    def more_info(self):
        
        more = dummy()
        more.id = self.id
        more.name = self.name

        cur_datetime = dt.datetime.combine(self.departure_date, self.departure_time)
        
        more.dep_date = cur_datetime.strftime('%A, %b %d, %Y')
        more.dep_time = cur_datetime.strftime('%-I:%M %p')
        more.dep = self.origin

        diff = dt.timedelta(minutes=self.duration)
        more.dur = f"{self.duration//60}hr {self.duration%60}m"
        cur_datetime += diff

        more.ari_date = cur_datetime.strftime('%A, %b %d, %Y')
        more.ari_time = cur_datetime.strftime('%-I:%M %p')
        more.ari = self.destination

        more.price = self.min_price

        return more



    def __repr__(self):
        return f"Flight('{self.name}', '{self.departure_date}', '{self.origin}', '{self.destination}')"


class Seat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    booked = db.Column(db.Boolean, nullable=False, default=False)

    book = db.relationship('Booking', backref='seat', lazy=True, cascade='all, delete', uselist=False)


    def book_seat(self, user_id):
        
        self.booked = True
        self.flight.avilable_seat -= 1

        db.session.add(Booking(seat_id=self.id, user_id=user_id))
        db.session.commit()

    def __repr__(self):
        flight_name = Flight.query.get(int(self.flight_id)).name
        return f"Seat('{flight_name}', '{self.name}', '{self.number}', '{self.price}', {self.booked})"

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'),unique=True, nullable=False)


    def cancel(self):
        
        self.seat.flight.avilable_seat += 1
        self.seat.booked = False
        
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        user_name = User.query.get(int(self.user_id)).name
        return f"Booking('{user_name}', '{self.seat_id}')"