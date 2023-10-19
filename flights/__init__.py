from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from collections import defaultdict

# import atexit
# import smtplib


# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()
# server.login("201501053@rajalakshmi.edu.in", "nohack1234@")

# @atexit.register
# def quit_smtp_server():
#     server.quit()


# class MailService:
#     def __init__(self):
#         self.qu = defaultdict(list)

#     def add(self, email, number):
#         self.qu[email].append(number)

#     def send(self, reason):

#         if reason == 'book':
#             msg = 'You have booked {} tickets.\nYour ticket numbers are {}.'
#         elif reason == 'cancel':
#             msg = 'You have Canceled {} tickets.\nTicket numbers are {}.'
#         else:
#             msg = 'Due to bad weather Your flight has been canceled\nCanceled ticket numbers are {}.'

#         for email in self.qu:
#             if email == 'admin':
#                 continue

#             msg.format(len(self.qu[email]), ', '.join(map(str, self.qu[email])))
#             del self.qu[email]

app = Flask(__name__)

app.config['SECRET_KEY'] = 'HighlysecureString'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flights import routes