from flask import render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, TeacherRegisterForm, CourseRegisterForm, ScheludeRegisterForm, SigninForm
from flask_login import login_user, login_required, current_user, logout_user
from models import db, Teacher, Course, User, Schelude
from config import app, login_manager
from functools import wraps

import os
import sys

images = UploadSet('images', IMAGES)
configure_uploads(app, images)
Bootstrap(app)

all_days = ('Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье')
telephone='+79313282819'
address='6 линия В.О. дом 61'
email='info@proiskusstvo.ru'
vk='https://vk.com/publicproiskusstvo'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.get_id() != str(1):
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
   data = Course.query.all()
   teachers = Teacher.query.all()
   schl = data_for_rsp()  
   return render_template(
      'index.html', 
      price=data, 
      teachers=teachers, 
      all_days=all_days, 
      schelude=schl,
      telephone=telephone,
      address=address,
      email=email,
      vk=vk
      )

@app.route('/admin', methods=['GET', 'POST'])
def sign():
   form = SigninForm()
   if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if not user:
            flash(message="Не верный email, попробуйте снова или обратитесть к своему администратору")
            return render_template('signin.html', form=form)
      if check_password_hash(user.password, form.password.data):
         login_user(user)
         return redirect(url_for('menu'))
      else:
            flash(message="Не верный пароль, попробуйте снова")
            return render_template("signin.html", form=form, logged_in=current_user.is_authenticated)
   return render_template('signin.html', form=form)

@app.route('/menu')
@login_required
def menu():
   return render_template('menu.html')

@app.route('/adduser', methods=['GET', 'POST'])
@admin_only
@login_required
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
@admin_only
@login_required
def delete_user(user_id):
   user_to_delete = User.query.get(user_id)
   db.session.delete(user_to_delete)
   db.session.commit()
   return redirect(url_for('add_user'))

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST" ])
@admin_only
@login_required
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
@login_required
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
@admin_only
@login_required
def delete_teacher(teacher_id):
   teacher_to_delete = Teacher.query.get(teacher_id)
   if teacher_to_delete.avatar != '/static/images/default.jpeg':
      os.remove(path=f'{sys.path[0]}{teacher_to_delete.avatar}')
   db.session.delete(teacher_to_delete)
   db.session.commit()
   return redirect(url_for('add_teacher'))

@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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
         price=form.price.data
      )
      db.session.add(new_course)
      db.session.commit()
      return redirect(url_for('add_course'))
   return render_template('addcourse.html', form=form, courses=courses)

@app.route('/delete_course/<int:course_id>')
@login_required
def delete_course(course_id):
   course_to_delete = Course.query.get(course_id)
   if course_to_delete.avatar != '/static/images/default_course.jpeg':
      os.remove(path=f'{sys.path[0]}{course_to_delete.avatar}')
   db.session.delete(course_to_delete)
   db.session.commit()
   return redirect(url_for('add_course'))

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def add_schelude():
   schelude = Schelude.query.order_by(Schelude.start_time.asc()).all()
   
   cname = [course.name for course in Course.query.all()]
   tname = [teacher.name for teacher in Teacher.query.all()]
   form = ScheludeRegisterForm()
   form.course_name.choices = cname
   form.teacher_name.choices = tname
   schl = data_for_rsp()

   if form.validate_on_submit():
      new_schelude = Schelude(
         teacher=form.teacher_name.data,
         start_time=form.time.data,
         day = form.day.data,
         course = form.course_name.data,
         end_time = form.end_time.data
         )
      db.session.add(new_schelude)
      db.session.commit()
      return redirect(url_for('add_schelude'))
   return render_template('schelude.html', form=form, schelude=schl, all_days=all_days, rsp=schelude)

@app.route('/delete_schelude/<int:schelude_id>')
@login_required
def remove_schelude(schelude_id):
   schelude = Schelude.query.get(schelude_id)
   db.session.delete(schelude)
   db.session.commit()
   return redirect(url_for('add_schelude'))

@app.route('/edit_schelude/<int:schelude_id>', methods=['GET', 'POST'])
@login_required
def edit_schelude(schelude_id):
   schelude = Schelude.query.order_by(Schelude.start_time.asc()).all()
   edit_schelude = Schelude.query.get(schelude_id)

   cname = [course.name for course in Course.query.all()]
   tname = [teacher.name for teacher in Teacher.query.all()]
   form = ScheludeRegisterForm(
      day=edit_schelude.day,
      time=edit_schelude.start_time,
      end_time=edit_schelude.end_time,
      course_name=edit_schelude.course,
      teacher_name=edit_schelude.teacher
   )

   form.course_name.choices = cname
   form.teacher_name.choices = tname
   schl = data_for_rsp()

   if form.validate_on_submit():
      edit_schelude.day = form.day.data
      edit_schelude.start_time = form.time.data
      edit_schelude.end_time = form.end_time.data
      edit_schelude.course = form.course_name.data
      edit_schelude.teacher = form.teacher_name.data
      db.session.commit()
      return redirect(url_for('add_schelude'))
   return render_template('schelude.html', form=form, schelude=schl, all_days=all_days, rsp=schelude)

def data_for_rsp():
   schelude = Schelude.query.order_by(Schelude.start_time.asc()).all()
   all_time = sorted({time.start_time for time in schelude})
   schl = {}

   for time in all_time:
      for data in schelude:
         if data.start_time == time:
            if data.start_time in schl:
               schl[time].update({data.day: [data.course, f'{data.start_time} - {data.end_time}']})
            else:
               schl[time] = {data.day: [data.course, f'{data.start_time} - {data.end_time}']}
   return schl

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('sign'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
