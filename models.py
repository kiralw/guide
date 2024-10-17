from . import db

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200))
