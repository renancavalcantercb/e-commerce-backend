from datetime import datetime
from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    on_sale = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.sale_price}', '{self.on_sale}', '{self.description}', '{self.image}', '{self.category}', '{self.quantity}', '{self.rating}', '{self.reviews}', '{self.date_added}')"


class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.password}', '{self.cpf}', '{self.birth_date}', '{self.phone}', '{self.admin}', '{self.date_added}')"
