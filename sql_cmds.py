import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# login signup
def register(email, password):

    cursor.execute("SELECT * FROM customer WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) != 0:
        return {"status": "bad", "msg": "Email already registered"}
    
    password = str(hash(password))

    cursor.execute("INSERT INTO customer (email, password_hashed) VALUES (?, ?)", (email, password,))
    conn.commit()

    return {"status": "good", "msg": "Reistered!"}


def login(email, password):

    cursor.execute("SELECT * FROM customer WHERE email = ?", (email,))
    
    already = cursor.fetchall()
    if len(already) == 0:
        return {"status": "bad", "msg": "email not found"}
    
    password = str(hash(password))

    if already[0][-1] != password:
        return {"status": "bad", "msg": "incorrect password"}

    return {"status": "good", "msg": "loggedin", "id":already[0][0]}


def admin_register(username, password):

    cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
    
    already = cursor.fetchall()
    if len(already) != 0:
        return {"status": "bad", "msg": "Username already registered"}
    
    password = str(hash(password))

    cursor.execute("INSERT INTO admin (username, password_hashed) VALUES (?, ?)", (username, password,))
    conn.commit()

    return {"status": "good", "msg": "Reistered!"}

def admin_login(username, password):

    cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
    
    already = cursor.fetchall()
    if len(already) == 0:
        return {"status": "bad", "msg": "username not found"}
    
    password = str(hash(password))

    if already[0][-1] != password:
        return {"status": "bad", "msg": "incorrect password"}

    return {"status": "good", "msg": "loggedin", "id":already[0][0]}


# flight add remove
