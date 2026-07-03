from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    guests = db.relationship('Guest', back_populates='event', cascade='all, delete-orphan')
    menu_items = db.relationship('EventMenu', back_populates='event', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'guest_count': len(self.guests),
            'menu_count': len(self.menu_items),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    event = db.relationship('Event', back_populates='guests')
    dietary_tags = db.relationship('GuestDietaryTag', back_populates='guest', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'name': self.name,
            'tags': [tag.tag for tag in self.dietary_tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class GuestDietaryTag(db.Model):
    __tablename__ = 'guest_dietary_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    
    guest = db.relationship('Guest', back_populates='dietary_tags')
    
    def to_dict(self):
        return {
            'id': self.id,
            'guest_id': self.guest_id,
            'tag': self.tag,
        }


class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    per_head_cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ingredients = db.relationship('DishIngredient', back_populates='dish', cascade='all, delete-orphan')
    menu_items = db.relationship('EventMenu', back_populates='dish')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'per_head_cost': self.per_head_cost,
            'description': self.description,
            'category': self.category,
            'ingredients': [di.ingredient.to_dict() for di in self.ingredients],
            'allergens': list(set([tag.tag for di in self.ingredients for tag in di.ingredient.allergen_tags])),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    allergen_tags = db.relationship('IngredientAllergenTag', back_populates='ingredient', cascade='all, delete-orphan')
    dish_ingredients = db.relationship('DishIngredient', back_populates='ingredient')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'allergen_tags': [tag.tag for tag in self.allergen_tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class IngredientAllergenTag(db.Model):
    __tablename__ = 'ingredient_allergen_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    
    ingredient = db.relationship('Ingredient', back_populates='allergen_tags')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ingredient_id': self.ingredient_id,
            'tag': self.tag,
        }


class DishIngredient(db.Model):
    __tablename__ = 'dish_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    
    dish = db.relationship('Dish', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='dish_ingredients')
    
    def to_dict(self):
        return {
            'id': self.id,
            'dish_id': self.dish_id,
            'ingredient_id': self.ingredient_id,
        }


class EventMenu(db.Model):
    __tablename__ = 'event_menu'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    event = db.relationship('Event', back_populates='menu_items')
    dish = db.relationship('Dish', back_populates='menu_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'dish_id': self.dish_id,
            'dish': self.dish.to_dict() if self.dish else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
