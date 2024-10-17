from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

print("Current directory:", os.getcwd())

# Инициализация SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    # Настройки для подключения к базе данных PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kira:123@localhost/plant_inventory'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация базы данных с приложением
    db.init_app(app)

    # Регистрация маршрутов через Blueprint
    from .routes import bp
    app.register_blueprint(bp)

    # Создание всех таблиц базы данных
    with app.app_context():
        db.create_all()

    return app
