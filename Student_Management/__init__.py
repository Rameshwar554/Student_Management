from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app1 = Flask(__name__)
mail = Mail(app1)
app1.secret_key = 'otp'


app1.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://system:system@127.0.0.1:1521/xe'
db = SQLAlchemy(app1)

app1.config["MAIL_SERVER"] = 'smtp.gmail.com'
app1.config["MAIL_PORT"] = 465
app1.config["MAIL_USERNAME"] = 'dummypass789@gmail.com'
app1.config['MAIL_PASSWORD'] = 'Dummy@00'       # you have to give your password of gmail account
app1.config['MAIL_USE_TLS'] = False
app1.config['MAIL_USE_SSL'] = True


from Student_Management import routes
