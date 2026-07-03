"""
Seed script to populate the database with sample data for testing.
Run with: python seed.py
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Event, Guest, GuestDietaryTag, Dish, Ingredient, IngredientAllergenTag, DishIngredient, EventMenu


def seed_database():
    """Populate database with sample data."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("✓ Database tables created")
        
        # Create ingredients
        ingredients_data = [
            ('chicken', ['meat']),
            ('beef', ['meat']),
            ('pork', ['meat']),
            ('salmon', ['meat', 'fish']),
            ('aubergine', []),
            ('zucchini', []),
            ('tomato', []),
            ('ricotta', ['dairy']),
            ('mozzarella', ['dairy']),
            ('parmesan', ['dairy']),
            ('eggs', ['eggs']),
            ('milk', ['dairy']),
            ('butter', ['dairy']),
            ('honey', ['honey']),
            ('wheat flour', ['gluten']),
            ('pasta', ['gluten']),
            ('rice', []),
            ('quinoa', []),
            ('almonds', ['nuts']),
            ('walnuts', ['nuts']),
            ('peanuts', ['nuts']),
            ('sesame', []),
            ('olive oil', []),
            ('herbs', []),
            ('berries', []),
            ('coconut', []),
            ('miso', ['gluten']),
        ]
        
        ingredients = {}
        for name, tags in ingredients_data:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)
            db.session.flush()
            
            for tag in tags:
                allergen = IngredientAllergenTag(ingredient_id=ingredient.id, tag=tag)
                db.session.add(allergen)
            
            ingredients[name] = ingredient
        
        db.session.commit()
        print(f"✓ Created {len(ingredients)} ingredients")
        
        # Create dishes
        dishes_data = [
            {
                'name': 'Citrus Herb Roasted Chicken',
                'cost': 14.00,
                'category': 'Signature',
                'description': 'Bright, crowd-pleasing roast with seasonal greens and a lemon glaze.',
                'ingredients': ['chicken', 'herbs', 'olive oil', 'rice'],
            },
            {
                'name': 'Miso-Glazed Aubergine',
                'cost': 11.00,
                'category': 'Plant-based',
                'description': 'Silky roasted eggplant with sesame crunch and herb rice.',
                'ingredients': ['aubergine', 'miso', 'sesame', 'rice'],
            },
            {
                'name': 'Market Vegetable Tart',
                'cost': 12.00,
                'category': 'Seasonal',
                'description': 'Buttery tart stacked with caramelized vegetables and whipped ricotta.',
                'ingredients': ['wheat flour', 'ricotta', 'zucchini', 'tomato', 'eggs', 'butter'],
            },
            {
                'name': 'Coconut Citrus Panna Cotta',
                'cost': 8.00,
                'category': 'Dessert',
                'description': 'Silky finale with macerated berries and toasted coconut.',
                'ingredients': ['coconut', 'berries', 'milk', 'honey'],
            },
            {
                'name': 'Charred Broccolini & Grain Bowl',
                'cost': 10.00,
                'category': 'Lunch',
                'description': 'Hearty, balanced bowl with quinoa, greens, and herb crunch.',
                'ingredients': ['quinoa', 'zucchini', 'sesame', 'herbs', 'olive oil'],
            },
            {
                'name': 'Grilled Salmon with Herbs',
                'cost': 16.00,
                'category': 'Signature',
                'description': 'Fresh-caught salmon with herb butter and seasonal vegetables.',
                'ingredients': ['salmon', 'herbs', 'butter', 'zucchini'],
            },
            {
                'name': 'Beef Tenderloin & Root Vegetables',
                'cost': 18.00,
                'category': 'Signature',
                'description': 'Premium cut with roasted vegetables and red wine reduction.',
                'ingredients': ['beef', 'herbs', 'olive oil', 'tomato', 'zucchini'],
            },
        ]
        
        dishes = {}
        for dish_data in dishes_data:
            dish = Dish(
                name=dish_data['name'],
                per_head_cost=dish_data['cost'],
                category=dish_data['category'],
                description=dish_data['description'],
            )
            db.session.add(dish)
            db.session.flush()
            
            for ingredient_name in dish_data['ingredients']:
                if ingredient_name in ingredients:
                    di = DishIngredient(dish_id=dish.id, ingredient_id=ingredients[ingredient_name].id)
                    db.session.add(di)
            
            dishes[dish_data['name']] = dish
        
        db.session.commit()
        print(f"✓ Created {len(dishes)} dishes")
        
        # Create events
        event1 = Event(
            name='Midsummer Gala',
            date='Saturday, August 17',
            description='Elegant outdoor summer celebration',
        )
        db.session.add(event1)
        db.session.flush()
        
        event2 = Event(
            name='Founders Brunch',
            date='Thursday, September 5',
            description='Corporate brunch for leadership team',
        )
        db.session.add(event2)
        db.session.flush()
        
        # Create guests for event1
        guest_data_event1 = [
            ('Avery Stone', ['vegetarian', 'gluten-free']),
            ('Jordan Lee', ['vegan']),
            ('Priya Shah', ['nut-allergy']),
            ('Mia Chen', ['gluten-free']),
            ('Alex Morgan', []),
            ('Casey Robinson', ['vegetarian']),
            ('Taylor Wright', ['vegan', 'gluten-free']),
            ('Morgan Green', []),
        ]
        
        for name, tags in guest_data_event1:
            guest = Guest(event_id=event1.id, name=name)
            db.session.add(guest)
            db.session.flush()
            
            for tag in tags:
                dt = GuestDietaryTag(guest_id=guest.id, tag=tag)
                db.session.add(dt)
        
        # Create guests for event2
        guest_data_event2 = [
            ('Sarah Allen', ['vegetarian']),
            ('Michael Brown', []),
            ('Lisa Chen', ['gluten-free']),
            ('David Martinez', []),
            ('Emily Wilson', ['vegan']),
        ]
        
        for name, tags in guest_data_event2:
            guest = Guest(event_id=event2.id, name=name)
            db.session.add(guest)
            db.session.flush()
            
            for tag in tags:
                dt = GuestDietaryTag(guest_id=guest.id, tag=tag)
                db.session.add(dt)
        
        db.session.commit()
        print("✓ Created 2 events with 13 guests total")
        
        # Add dishes to event menus
        event1_dishes = [
            'Citrus Herb Roasted Chicken',
            'Miso-Glazed Aubergine',
            'Market Vegetable Tart',
            'Coconut Citrus Panna Cotta',
        ]
        
        for dish_name in event1_dishes:
            menu_item = EventMenu(event_id=event1.id, dish_id=dishes[dish_name].id)
            db.session.add(menu_item)
        
        event2_dishes = [
            'Grilled Salmon with Herbs',
            'Charred Broccolini & Grain Bowl',
            'Beef Tenderloin & Root Vegetables',
        ]
        
        for dish_name in event2_dishes:
            menu_item = EventMenu(event_id=event2.id, dish_id=dishes[dish_name].id)
            db.session.add(menu_item)
        
        db.session.commit()
        print("✓ Added dishes to event menus")
        
        print("\n✅ Database seeding complete!")
        print(f"   - {len(ingredients)} ingredients")
        print(f"   - {len(dishes)} dishes")
        print(f"   - 2 events")
        print(f"   - 13 guests")
        print("\nDatabase ready at: event_catering.db")


if __name__ == '__main__':
    seed_database()
