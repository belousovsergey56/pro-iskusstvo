from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app import Teacher, Course

class RegisterForm(FlaskForm):
    name = StringField(label='', render_kw={'placeholder': 'Имя пользователя'} ,validators=[DataRequired()])
    email = StringField(label='', render_kw={'placeholder': 'Электронная почта'}, validators=[DataRequired()])
    password = PasswordField(label='', render_kw={'placeholder': 'Пароль'}, validators=[DataRequired()])
    sign = SubmitField('Добавить пользователя')

class TeacherRegisterForm(FlaskForm):
    name = StringField(label='', render_kw={'placeholder': 'Имя преподавателя'} ,validators=[DataRequired()])
    description = TextAreaField(label='', render_kw={'placeholder': 'О преподавателе'} ,validators=[DataRequired()])
    path_photo = FileField(label='Загрузить фото')
    submit = SubmitField('Добавить преподавателя')

class CourseRegisterForm(FlaskForm):
    name = StringField(label='', render_kw={'placeholder': 'Название курса'} ,validators=[DataRequired()])
    description = TextAreaField(label='', render_kw={'placeholder': 'Описание курса'} ,validators=[DataRequired()])
    price = StringField(label='', render_kw={'placeholder': 'Стоимость курса'} ,validators=[DataRequired()])
    path_photo = FileField(label='Загрузить фото курса')
    enter = SubmitField('Добавить курс')

class ScheludeRegisterForm(FlaskForm):
    course = [_course.name for _course in Course.query.all()]
    teacher = [_teacher.name for _teacher in Teacher.query.all()]

    day = SelectField(label='', render_kw={'placeholder': 'Выбрать день проведения курса'}, choices=['Понедельник', 'Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'])
    time = StringField('', render_kw={'placeholder': 'Дата начала занятий (формат: 11:00, 21:15, 13:45)'})
    course_name = SelectField(label='Название курса', choices=course)
    teacher_name = SelectField(label='Выбрать преподавателя', choices=Teacher)
    add_schelude = SubmitField('Добавить курс в расписание')
    