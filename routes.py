from flask import render_template, Blueprint, redirect, url_for, request
from .models import Plant
from . import db
import os

# Создание экземпляра Blueprint
bp = Blueprint('main', __name__)

# Маршрут для главной страницы, который перенаправляет на страницу с растениями
@bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.get_plants'))

# Маршрут для страницы с растениями
@bp.route('/plants', methods=['GET'])
def get_plants():
    search_query = request.args.get('search')  # Получение параметра поиска из URL
    if search_query:
        plants = Plant.query.filter(
            (Plant.name.ilike(f'%{search_query}%')) |
            (Plant.species.ilike(f'%{search_query}%'))
        ).all()  # Фильтрация растений по названию или виду
    else:
        plants = Plant.query.all()  # Получение всех растений из базы данных
    return render_template('plants.html', plants=plants)  # Возврат шаблона с данными

# Маршрут для добавления нового растения
@bp.route('/plants', methods=['POST'])
def add_plant():
    name = request.form['name']
    species = request.form['species']
    purchase_date = request.form['purchase_date']
    location = request.form['location']
    image = request.files['image']

    # Сохранение изображения
    image_url = None
    if image:
        print(f"Загружено изображение: {image.filename}")  # Вывод имени файла на консоль
        image_path = os.path.join('app/static/images', image.filename)  # Путь для сохранения изображения

        # Проверка на существование директории
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        image.save(image_path)  # Сохранение изображения
        image_url = f'images/{image.filename}'  # Сохраняем относительный путь для доступа к изображению

    # Добавление нового растения в базу данных
    new_plant = Plant(name=name, species=species, purchase_date=purchase_date, location=location, image_url=image_url)
    db.session.add(new_plant)
    db.session.commit()

    return redirect(url_for('main.get_plants'))

# Маршрут для удаления растения
@bp.route('/plants/delete/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    plant = Plant.query.get(plant_id)  # Получение растения по ID
    if plant:
        db.session.delete(plant)  # Удаление растения из базы данных
        db.session.commit()  # Сохранение изменений
        print(f"Удалено растение: {plant.name}")  # Отладочное сообщение
    return redirect(url_for('main.get_plants'))
