# flight-devrev
Round 2 flight booking application

## SQL tables
```
admin
customers
flights
bookings
```

## setup
```
git clone https://github.com/sunilxd/flight-devrev.git
pip install sqlite3
pip install tabulate
```

## To run
```
cd flight-devrev
python main.py
```

## Commands
### general
- `show` - print the table
- `flights` - search flight with given date and time
- `logout` - logout the user

### admin
- `admin_login` - login as admin
- `admin_register` - register admin account
- `add` - add flight
- `remove` - remove flight
- `tickets` - return booked tickets given `flight_id`

### customer
- `login` - login as customer
- `register` - register a account
- `book` - book a flight
- `cancel` - cancel a booked ticket
- `myorder` - return all the ticket booked by the user

## Syntax
```
show table_name
show flights

logout
logout

admin_register username password
admin_register admin admin

register email password
register sunil@gmail.com sunil

admin_login username password
admin_login admin admin

login username password
login sunil@gmail.com sunil

add flight_name departure_date departure_time duration origin destination price seats_available
add Unite_Airlines 2023-05-22 10:00 3.5 New_York Los_Angeles 500 60

remove flight_id
remove 1

flights date time
flights 2023-05-22 10:00:00

book flight_id number_of_tickets
book 1 2

cancel booking_id
cancel 1

myorder
myorder

tickets flight_id
tickets 1
```


## Database schema
```sqlite

CREATE TABLE IF NOT EXISTS "customers" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  password_hashed TEXT NOT NULL
);


CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password_hashed TEXT NOT NULL
);


CREATE TABLE flight_company (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);


CREATE TABLE flights (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_id INTEGER NOT NULL,
  departure_date DATE NOT NULL,
  departure_time TIME NOT NULL,
  origin TEXT NOT NULL,
  destination TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, seats_available INT NOT NULL, duration DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (company_id) REFERENCES flight_company (id)
);


CREATE TABLE bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  flight_id INTEGER NOT NULL,
  number_of_tickets INTEGER NOT NULL,
  status TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (flight_id) REFERENCES flights(id)
);


CREATE TRIGGER reduce_available_seats_and_confirm_booking
AFTER INSERT ON bookings
BEGIN
    UPDATE flights
    SET seats_available = seats_available - NEW.number_of_tickets
    WHERE id = NEW.flight_id;

    UPDATE bookings
    SET status = 'Confirmed'
    WHERE id = NEW.id;
END;

```