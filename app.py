from hashlib import sha1
from operator import length_hint
from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads, IMAGES, UploadSet
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, TeacherRegisterForm, CourseRegisterForm, ScheludeRegisterForm

from models import db, Teacher, Course, User, Schedule
from config import app

import os
import sys
import json

# Имплементация экземпляра объекта UloadSet, добавление в конфигурацию приложение и экземляр класса, подключение bootstrap
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
Bootstrap(app)

# Добавление в конфиги приложения базы данных, имплементация объекта класса SQLAlchemy, подключение ORM


@app.route('/')
def home():
   d = {'понедельник': {'11:15':'belousov'}, 'вторник': {'12:00': 'zuenko'}, 'среда': {'11:00': 'saul'}}
   data = Course.query.all()
   teachers = Teacher.query.all()
   return render_template('index.html', price=data, teachers=teachers, d=d)

@app.route('/admin')
def sign():
   return render_template('signin.html')

@app.route('/menu')
def menu():
   return render_template('menu.html')

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
   form = RegisterForm()
   users = User.query.all()
   if form.validate_on_submit():
      if User.query.filter_by(email=form.user_email.data).first():
         flash(message='Пользователь с такой почтой уже существует, попробуйте ввести новую почту')
         return redirect(url_for('add_user'))
      new_user = User(
         name = form.user_name.data,
         email = form.user_email.data,
         password = generate_password_hash(form.password.data, salt_length=13)
      )
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('add_user'))
   return render_template('adduser.html', form=form, users=users)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
   user_to_delete = User.query.get(user_id)
   db.session.delete(user_to_delete)
   db.session.commit()
   return redirect(url_for('add_user'))

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST" ])
def edit_user(user_id):
   users = User.query.all()
   user = User.query.get(user_id)
   edit_form= RegisterForm(
      user_name=user.name,
      user_email=user.email
      )

   if edit_form.validate_on_submit():
      user.name = edit_form.user_name.data
      user.email = edit_form.user_email.data
      user.password = generate_password_hash(edit_form.password.data, salt_length=13)
      db.session.commit()
      return redirect(url_for('add_user'))
   return render_template('adduser.html', form=edit_form, users=users)
   

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
   teacher = Teacher.query.order_by(Teacher.id.asc()).all()
   form = TeacherRegisterForm()
   if form.validate_on_submit():
      if form.path_photo.data:
         filename = images.save(form.path_photo.data)
      new_teacher = Teacher(
         name=form.name.data,
         avatar=f'/static/images/{filename}' if form.path_photo.data else '/static/images/default.jpeg',
         about=form.description.data
      )
      db.session.add(new_teacher)
      db.session.commit()
      return redirect(url_for('add_teacher'))
   return render_template('addteacher.html', form=form, teachers=teacher)

@app.route('/delete_teacher/<int:teacher_id>')
def delete_teacher(teacher_id):
   teacher_to_delete = Teacher.query.get(teacher_id)
   if teacher_to_delete.avatar != '/static/images/default.jpeg':
      os.remove(path=f'{sys.path[0]}{teacher_to_delete.avatar}')
   db.session.delete(teacher_to_delete)
   db.session.commit()
   return redirect(url_for('add_teacher'))

@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
   all_teachers = Teacher.query.order_by(Teacher.id.asc()).all()
   teacher = Teacher.query.get(teacher_id)
   form = TeacherRegisterForm(
      name=teacher.name,
      description=teacher.about,
      path_photo=teacher.avatar
   )
   if form.validate_on_submit():
      if form.path_photo.data:
         filename = images.save(form.path_photo.data)
         if teacher.avatar != '/static/images/default.jpeg':
            os.remove(path=f'{sys.path[0]}{teacher.avatar}')
      teacher.name = form.name.data
      teacher.about = form.description.data
      teacher.avatar = f'/static/images/{filename}' if form.path_photo.data else teacher.avatar
      db.session.commit()
      return redirect(url_for('add_teacher'))
   return render_template('addteacher.html', form=form, teachers=all_teachers)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
   courses = Course.query.order_by(Course.id.asc()).all()
   form = CourseRegisterForm()
   if form.validate_on_submit():
      if form.path_photo.data:
         filename = images.save(form.path_photo.data)
      new_course = Course(
         name=form.name.data,
         avatar=f'/static/images/{filename}' if form.path_photo.data else '/static/images/default_course.jpeg',
         description=form.description.data,
         price=int(form.price.data)
      )
      db.session.add(new_course)
      db.session.commit()
      return redirect(url_for('add_course'))
   return render_template('addcourse.html', form=form, courses=courses)

@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
   course_to_delete = Course.query.get(course_id)
   if course_to_delete.avatar != '/static/images/default_course.jpeg':
      os.remove(path=f'{sys.path[0]}{course_to_delete.avatar}')
   db.session.delete(course_to_delete)
   db.session.commit()
   return redirect(url_for('add_course'))

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
   courses = Course.query.all()
   edit_course = Course.query.get(course_id)
   form = CourseRegisterForm(
      name= edit_course.name,
      description=edit_course.description,
      price=edit_course.price,
      path_photo=edit_course.avatar
   )
   if form.validate_on_submit():
      if form.path_photo.data:
         filename = images.save(form.path_photo.data)
         if edit_course.avatar != '/static/images/default_course.jpeg':
            os.remove(path=f'{sys.path[0]}{edit_course.avatar}')
      edit_course.name = form.name.data
      edit_course.description = form.description.data
      edit_course.avatar = f'/static/images/{filename}' if form.path_photo.data else edit_course.avatar
      edit_course.price = form.price.data
      db.session.commit()
      return redirect(url_for('add_course'))
   return render_template('addcourse.html', form=form, courses=courses)

@app.route('/add_schelude', methods=['GET', 'POST'])
def add_schelude():
   schelude = Schedule.query.order_by(Schedule.time.asc()).all()
   all_time = [time.time for time in schelude]
   all_days = [day.day for day in schelude]
   cname = [course.name for course in Course.query.all()]
   tname = [teacher.name for teacher in Teacher.query.all()]

   form = ScheludeRegisterForm()
   form.course_name.choices = cname
   form.teacher_name.choices = tname

   if form.validate_on_submit():
      new_schelude = Schedule(
         course=form.course_name.data,
         teacher=form.teacher_name.data,
         time=form.time.data,
         day = form.day.data
         )
      db.session.add(new_schelude)
      db.session.commit()
      return redirect(url_for('add_schelude'))
   return render_template('schelude.html', form=form, schelude=schelude, all_time=all_time, all_days=all_days)
