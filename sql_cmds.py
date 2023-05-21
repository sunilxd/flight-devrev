import sqlite3
import hashlib

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

        cursor.close()
        conn.close()

        return response
    
    return wrapper


# login signup
@with_cursor
def register(conn, cursor, email, password):

    cursor.execute("SELECT * FROM customer WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) != 0:
        return {"status": "bad", "msg": "Email already registered"}
    
    password = hash_input(password)

    cursor.execute("INSERT INTO customer (email, password_hashed) VALUES (?, ?)", (email, password,))
    conn.commit()

    return {"status": "good", "msg": "Registered!"}


@with_cursor
def login(conn, cursor, email, password):

    cursor.execute("SELECT * FROM customer WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) == 0:
        return {"status": "bad", "msg": "email not found"}
    
    password = hash_input(password)

    if already[0][-1] != password:
        return {"status": "bad", "msg": "incorrect password"}

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

    return {"status": "good", "msg": "loggedin", "id":already[0][0]}


# add flight company
@with_cursor
def list_company(conn, cursor):

    cursor.execute("SELECT * FROM flight_company")
    return [flight[1] for flight in cursor.fetchall()]


@with_cursor
def add_company(conn, cursor, company_name):

    cursor.execute("SELECT * FROM flight_company WHERE name = ?", (company_name, ))
    
    if len(cursor.fetchall()) != 0:
        return {"status": "bad", "msg": f"{company_name} already added"}

    cursor.execute("INSERT INTO flight_company (name) VALUES (?)", (company_name, ))
    conn.commit()

    return {"status": "good", "msg": f"{company_name} added"}


# add flights
