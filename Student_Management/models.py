from Student_Management import db


class Student(db.Model):
    stuid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    marks = db.Column(db.Integer(), unique=False, nullable=False)
