from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, EmailField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class SigninForm(FlaskForm):
    email = EmailField(label='', render_kw={'placeholder': 'Электронная почта'} ,validators=[DataRequired()])
    password = PasswordField(label='', render_kw={'placeholder': 'Пароль'} ,validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    user_name = StringField(label='', render_kw={'placeholder': 'Имя пользователя'} ,validators=[DataRequired()])
    user_email = StringField(label='', render_kw={'placeholder': 'Электронная почта'}, validators=[DataRequired()])
    password = PasswordField(label='', render_kw={'placeholder': 'Пароль'}, validators=[DataRequired()])
    sign = SubmitField('Добавить пользователя')

class TeacherRegisterForm(FlaskForm):
    name = StringField(label='', render_kw={'placeholder': 'Имя преподавателя'} ,validators=[DataRequired()])
    description = CKEditorField(label='', render_kw={'placeholder': 'О преподавателе'} ,validators=[DataRequired()])
    path_photo = FileField(label='Загрузить фото')
    submit = SubmitField('Добавить преподавателя')

class CourseRegisterForm(FlaskForm):
    name = StringField(label='', render_kw={'placeholder': 'Название курса'} ,validators=[DataRequired()])
    description = TextAreaField(label='', render_kw={'placeholder': 'Описание курса'} ,validators=[DataRequired()])
    price = StringField(label='', render_kw={'placeholder': 'Стоимость курса'} ,validators=[DataRequired()])
    path_photo = FileField(label='Загрузить фото курса')
    enter = SubmitField('Добавить курс')

class ScheludeRegisterForm(FlaskForm):
    day = SelectField(label='', render_kw={'placeholder': 'Выбрать день проведения курса'}, choices=['Понедельник', 'Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'])
    time = StringField('', render_kw={'placeholder': 'Время начала занятий (формат: 11:00, 21:15, 13:45)'})
    end_time = StringField('', render_kw={'placeholder': 'Время окончания занятий (формат: 11:00, 21:15, 13:45)'})
    course_name = SelectField(label='Название курса')
    teacher_name = SelectField(label='Выбрать преподавателя')
    add_schelude = SubmitField('Добавить курс в расписание')
    