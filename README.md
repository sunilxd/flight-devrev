# flight-devrev
Round 2 flight booking application


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