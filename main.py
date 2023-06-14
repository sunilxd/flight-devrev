import sqlite3
import hashlib
from tabulate import tabulate

def hash_input(input_text):

    hash_object = hashlib.sha256()
    hash_object.update(input_text.encode("utf-8"))
    hash_value = hash_object.hexdigest()

    return hash_value


# to avoid multiple thread error
def with_cursor(func):

    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        response = func(conn, cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()

        return response
    
    return wrapper


person = {
    "is_logged_in": False, "id": "", "admin": False
}


def logout():
    global person

    person = {
        "is_logged_in": False, "id": "", "admin": False
    }

    return {"status": "good", "msg": "loggedout"}


# login signup
@with_cursor
def register(conn, cursor, email, password):

    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) != 0:
        return {"status": "bad", "msg": "Email already registered"}
    
    password = hash_input(password)

    cursor.execute("INSERT INTO customers (email, password_hashed) VALUES (?, ?)", (email, password,))
    conn.commit()

    return {"status": "good", "msg": "Registered!"}


@with_cursor
def login(conn, cursor, email, password):

    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) == 0:
        return {"status": "bad", "msg": "email not found"}
    
    password = hash_input(password)

    if already[0][-1] != password:
        return {"status": "bad", "msg": "incorrect password"}
    
    global person

    person["is_logged_in"] = True
    person["id"] = already[0][0]

    return {"status": "good", "msg": "loggedin", "id":already[0][0]}


@with_cursor
def admin_register(conn, cursor, username, password):

    cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
    
    already = cursor.fetchall()
    if len(already) != 0:
        return {"status": "bad", "msg": "Username already registered"}
    
    password = hash_input(password)

    cursor.execute("INSERT INTO admin (username, password_hashed) VALUES (?, ?)", (username, password,))
    conn.commit()

    return {"status": "good", "msg": "Reistered!"}

@with_cursor
def admin_login(conn, cursor, username, password):

    cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
    
    already = cursor.fetchall()
    if len(already) == 0:
        return {"status": "bad", "msg": "username not found"}
    
    password = hash_input(password)

    if already[0][-1] != password:
        return {"status": "bad", "msg": "incorrect password"}
    
    global person
    
    person["is_logged_in"] = True
    person["id"] = already[0][0]
    person["admin"] = True

    return {"status": "good", "msg": "loggedin", "id":already[0][0]}



# add remove flight flights
@with_cursor
def add(conn, cursor, flight_name, departure_date, departure_time, duration, origin, destination, price, seats_available):

    duration = float(duration)
    price = float(price)
    seats_available = int(seats_available)

    if not person["admin"]:
        return {"status": "bad", "msg": "admin account needed"}
    
    try:
        cursor.execute(
            'INSERT INTO flights (flight_name, departure_date, departure_time, origin, destination, price, seats_available, duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (flight_name, departure_date, departure_time, origin, destination, price, seats_available, duration)
        )

        conn.commit()

        return {"status": "good", "msg": "Added"}
    
    except Exception as e:
        return {"status": "bad", "msg": f"error: {e}"}


@with_cursor
def remove(conn, cursor, flight_id):

    if not person["admin"]:
        return {"status": "bad", "msg": "admin account needed"}

    cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
    cursor.execute('DELETE FROM bookings WHERE flight_id = ?', (flight_id,))

    conn.commit()

    return {"status": "good", "msg": "Removed"}
    

@with_cursor
def book(conn, cursor, flight_id, number_of_tickets):

    number_of_tickets = int(number_of_tickets)

    if not person["is_logged_in"]:
        return {"status": "bad", "msg": "login first"}
    
    if person["admin"]:
        return {"status": "bad", "msg": "only customers can do this operation"}
    
    customer_id = person["id"]

    cursor.execute("SELECT seats_available FROM flights WHERE id = ?", (flight_id,))
    
    available = cursor.fetchall()

    if len(available) == 0:
        return {"status": "bad", "msg": "Flight not found"}
    
    available = available[0][0]
    
    if available < number_of_tickets:
        return {"status": "bad", "msg": f"Only {available} seats free"}

    try:
        cursor.execute(
            'INSERT INTO bookings (customer_id, flight_id, number_of_tickets, status) VALUES (?, ?, ?, ?)',
            (customer_id, flight_id, number_of_tickets, "Pending")
        )

        conn.commit()

        return {"status": "good", "msg": "Booked check you orders"}
    
    except Exception as e:
        return {"status": "bad", "msg": f"error: {e}"}
    

@with_cursor
def cancel(conn, cursor, booking_id):

    if not person["is_logged_in"]:
        return {"status": "bad", "msg": "login first"}
    
    if person["admin"]:
        return {"status": "bad", "msg": "only customers can do this operation"}
    
    customer_id = person["id"]

    cursor.execute("SELECT flight_id, number_of_tickets, status FROM bookings WHERE id = ? AND customer_id = ?", (booking_id, customer_id,))
    
    response = cursor.fetchall()

    if len(response) == 0:
        return {"status": "bad", "msg": "Invalid booking id"}
    
    flight_id, seat, booking = response[0][0], response[0][1], response[0][2]
    
    if booking == "Canceled":
        return {"status": "bad", "msg": "Already canceled"}
    
    ## cancel and change the availble seats
    cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', ('Canceled', booking_id))

    cursor.execute("UPDATE flights SET seats_available = seats_available + ? WHERE id = ?", (seat, flight_id))
    
    conn.commit()
    
    return {"status": "good", "msg": "Ticket Canceled"}


# my ticket
@with_cursor
def myorder(conn, cursor):

    if not person["is_logged_in"]:
        return {"status": "bad", "msg": "login first"}
    
    if person["admin"]:
        return {"status": "bad", "msg": "only customers can do this operation"}
    
    customer_id = person["id"]

    cursor.execute('SELECT * FROM bookings WHERE customer_id = ?', (customer_id,))
    column_names = [desc[0] for desc in cursor.description]

    values = cursor.fetchall()

    print(tabulate(values, headers=column_names))


@with_cursor
def show(conn, cursor, table_name):

    if not person["is_logged_in"]:
        return {"status": "bad", "msg": "login first"}

    cursor.execute(f"SELECT * FROM {table_name}")

    column_names = [desc[0] for desc in cursor.description]

    values = cursor.fetchall()

    print(tabulate(values, headers=column_names))


@with_cursor
def tickets(conn, cursor, flight_id):

    if not person["admin"]:
        return {"status": "bad", "msg": "admin only allowed"}

    cursor.execute("SELECT * FROM bookings WHERE flight_id = ?", (flight_id, ))

    column_names = [desc[0] for desc in cursor.description]

    values = cursor.fetchall()

    print(tabulate(values, headers=column_names))


@with_cursor
def flights(conn, cursor, date, time):

    if not person["is_logged_in"]:
        return {"status": "bad", "msg": "login first"}

    cursor.execute("SELECT * FROM flights WHERE departure_date >= ? AND departure_time >= ?", (date, time, ))

    column_names = [desc[0] for desc in cursor.description]

    values = cursor.fetchall()

    print(tabulate(values, headers=column_names))


# while True:

#     line = input('>>> ').split(' ')

#     function_name = line[0]
#     parameters = line[1:]

#     for i in range(len(parameters)):
#         parameters[i] = '"'+parameters[i]+'"'

#     try:

#         result = eval(function_name + '(' + ','.join(parameters) + ')')

#         print(result)

#     except Exception as e:
        
#         print(e)

#     print()
