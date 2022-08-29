from config import db
from flask_login import UserMixin


# Создание моделей для базы данных: Пользователь,Преподаватель, Курс, Расписание занятий 
class User(UserMixin, db.Model):
   __tablename__ = "users"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(1000))
   email = db.Column(db.String(100), unique=True)
   password = db.Column(db.String(1000))

class Teacher(db.Model):
   __tablename__ = "teachers"
   id = db.Column(db.Integer, primary_key=True)
   avatar = db.Column(db.String(1000))
   name = db.Column(db.String(1000))
   about = db.Column(db.String(1000))

class Course(db.Model):
   __tablename__ = 'courses'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100))
   avatar = db.Column(db.String(1000))
   description = db.Column(db.String(1000))
   price = db.Column(db.Integer)

class Schelude(db.Model):
   __tablename__ = 'scheludes'
   id = db.Column(db.Integer, primary_key=True)
   course = db.Column(db.String(100))
   teacher = db.Column(db.String(100))
   day = db.Column(db.String(100))
   start_time = db.Column(db.String(10))
   end_time = db.Column(db.String(100)) 


db.create_all()
