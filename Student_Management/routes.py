from flask import *
from flask_sqlalchemy import SQLAlchemy, request
from twilio.rest import Client                          # for mobile otp
from random import *                                    # for mobile otp and for email also
from flask_mail import Mail, Message
import random

from Student_Management.Conversation import start_chat
from Student_Management import app1, db
from Student_Management.models import Student


@app1.route('/')
def home():
    return render_template("student_login.html")


@app1.route('/')
def welcome_page():
    return render_template("Welcome.html")


# ADDING STUDENT
@app1.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        stuid = request.form.get('stuid')
        name = request.form.get('name')
        marks = request.form.get('marks')

        entry = Student(stuid=stuid, name=name, marks=marks)
        db.session.add(entry)
        db.session.commit()

    return render_template("add_student.html")


# DELETING STUDENT
@app1.route("/delete", methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        stuid = request.form.get('stuid')
        student = Student.query.filter_by(stuid=stuid).first()
        db.session.delete(student)
        db.session.commit()

    return render_template("delete.html")


# DELETING USING REST API
@app1.route("/delete/<int:stuid>", methods=['GET', 'POST'])
def delete_student_rest(stuid):
    student = Student.query.get(stuid)
    db.session.delete(student)
    db.session.commit()

    return "<center><h3>Deleted Successfully Using Rest API</h3></center>"


# UPDATE STUDENT
@app1.route("/update_student", methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        oldstuid = request.form.get('oldstuid')
        newstuid = request.form.get('newstuid')

        newname = request.form.get('newname')

        newmarks = request.form.get('newmarks')

        student = Student.query.filter_by(stuid=oldstuid).first()

        student.stuid = newstuid
        student.name = newname
        student.marks = newmarks
        db.session.commit()

    return render_template("update.html")


# UPDATE USING REST API
@app1.route("/update_student/<int:stuid>", methods=['GET', 'POST'])
def update_student_rest(stuid):
    student = Student.query.filter_by(stuid=stuid).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            stuid = request.form['stuid']
            name = request.form['name']
            marks = request.form['marks']
            student = Student(stuid=stuid, name=name, marks=marks)
            db.session.add(student)
            db.session.commit()

    return render_template("update_rest.html", student=student)


@app1.route("/logout")
def logout():
    if "user_id2" in session:
        session.pop("user_id2", None)
    return render_template("student_login.html")


# DISPLAY ALL DATA IN ONE PAGE AND SEARCH A PARTICULAR STUDENT
@app1.route("/display", methods=['GET', 'POST'])
def display():
    students = Student.query.order_by(Student.stuid.asc())
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        students = Student.query.filter(Student.name.like(search))
        return render_template("display_info.html", students=students, tag=tag)

    return render_template("display_info.html", students=students)


# USING PAGINATION AND REST API
@app1.route("/display/<int:page_num>")
def display_page(page_num):
    students = Student.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template("display_test.html", students=students)


# MOBILE LOGIN
@app1.route('/mobile_login')
def mobile_login():
    return render_template("mobile_login.html")


@app1.route("/get_otp", methods=['GET', 'POST'])
def get_otp():
    number = request.form['number']
    val = get_otp_api(number)
    if val:
        return render_template("enter_otp.html")


@app1.route('/validate_otp', methods=['POST'])
def validate_otp():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)
        if s == otp:
            return render_template("Welcome.html")
        else:
            return "You Are Not Authorized Sorry!!!"


def generate_otp():
    return random.randrange(100000, 999999)


def get_otp_api(number):
    account_sid = 'AC1db974f60f7af09f632246b976cdda6e'
    auth_token = 'f6211e284351ebb63a01f56579725963'
    client = Client(account_sid, auth_token)
    otp = generate_otp()
    session['response'] = str(otp)
    body = 'Your OTP is ' + str(otp)
    message = client.messages.create(from_='+16207431805', body=body, to=number)
    if message.sid:
        return True
    else:
        return False


# EMAIL LOGIN
mail = Mail(app1)


def generate():
    return random.randrange(100000, 999999)


otp = generate()


@app1.route('/email_login')
def email_login():
    return render_template("email_index.html")


@app1.route('/verify', methods=["POST"])
def verify():
    email = request.form['email']
    msg = Message(subject='OTP', sender='dummypass789@gmail.com', recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('email_verify.html')


@app1.route('/validate', methods=['POST'])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        return render_template("Welcome.html")
    return "<center><h3>Please Try Again</h3></center>"


# CHAT BOT
@app1.route('/chat_bot', methods=['GET', 'POST'])
def start_page():
    user_input = ""
    if request.method == 'POST':
        user_input = request.form['user_input'].lower()
        bot_response = start_chat(user_input)
        return render_template("chat_bot.html", bot_response=bot_response)
    else:
        return render_template("chat_bot.html")
