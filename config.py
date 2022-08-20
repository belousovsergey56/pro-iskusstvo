from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
# import _mysql_connector
from flask_login import LoginManager

load_dotenv()
db_password = os.getenv('mysql_password_root')



# Подключение фреймворка, добавление в конфиг серетнвый ключ, адрес загрузки картинок
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOADED_IMAGES_DEST'] = 'static/images'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///repinart.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://root:{db_password}@localhost/repin_art"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)
