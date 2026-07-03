from flask import Blueprint, request, jsonify
from models import db, Dish, Ingredient, IngredientAllergenTag, DishIngredient
from sqlalchemy.exc import SQLAlchemyError

dishes_bp = Blueprint('dishes', __name__, url_prefix='/api')


@dishes_bp.route('/dishes', methods=['GET'])
def list_dishes():
    """Get all dishes."""
    try:
        dishes = Dish.query.all()
        return jsonify([dish.to_dict() for dish in dishes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dishes_bp.route('/dishes', methods=['POST'])
def create_dish():
    """Create a new dish."""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        if 'per_head_cost' not in data:
            return jsonify({'error': 'Per head cost is required'}), 400
        
        dish = Dish(
            name=data['name'],
            per_head_cost=float(data['per_head_cost']),
            description=data.get('description', ''),
            category=data.get('category', '')
        )
        
        db.session.add(dish)
        db.session.flush()
        
        # Add ingredients
        ingredients = data.get('ingredients', [])
        for ingredient_id in ingredients:
            ingredient = Ingredient.query.get(ingredient_id)
            if ingredient:
                dish_ingredient = DishIngredient(
                    dish_id=dish.id,
                    ingredient_id=ingredient_id
                )
                db.session.add(dish_ingredient)
        
        db.session.commit()
        
        return jsonify(dish.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dishes_bp.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    """Get dish by ID."""
    try:
        dish = Dish.query.get(dish_id)
        
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        return jsonify(dish.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dishes_bp.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    """Update a dish."""
    try:
        dish = Dish.query.get(dish_id)
        
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            dish.name = data['name']
        if 'per_head_cost' in data:
            dish.per_head_cost = float(data['per_head_cost'])
        if 'description' in data:
            dish.description = data['description']
        if 'category' in data:
            dish.category = data['category']
        
        # Update ingredients if provided
        if 'ingredients' in data:
            DishIngredient.query.filter_by(dish_id=dish_id).delete()
            for ingredient_id in data['ingredients']:
                ingredient = Ingredient.query.get(ingredient_id)
                if ingredient:
                    dish_ingredient = DishIngredient(
                        dish_id=dish_id,
                        ingredient_id=ingredient_id
                    )
                    db.session.add(dish_ingredient)
        
        db.session.commit()
        
        return jsonify(dish.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dishes_bp.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    """Delete a dish."""
    try:
        dish = Dish.query.get(dish_id)
        
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        db.session.delete(dish)
        db.session.commit()
        
        return jsonify({'message': 'Dish deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dishes_bp.route('/ingredients', methods=['GET'])
def list_ingredients():
    """Get all ingredients."""
    try:
        ingredients = Ingredient.query.all()
        return jsonify([ingredient.to_dict() for ingredient in ingredients]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dishes_bp.route('/ingredients', methods=['POST'])
def create_ingredient():
    """Create a new ingredient."""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if ingredient already exists
        existing = Ingredient.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Ingredient already exists'}), 409
        
        ingredient = Ingredient(name=data['name'])
        db.session.add(ingredient)
        db.session.flush()
        
        # Add allergen tags
        tags = data.get('allergen_tags', [])
        for tag in tags:
            allergen = IngredientAllergenTag(
                ingredient_id=ingredient.id,
                tag=tag
            )
            db.session.add(allergen)
        
        db.session.commit()
        
        return jsonify(ingredient.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dishes_bp.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient by ID."""
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        
        if not ingredient:
            return jsonify({'error': 'Ingredient not found'}), 404
        
        return jsonify(ingredient.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dishes_bp.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    """Update an ingredient."""
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        
        if not ingredient:
            return jsonify({'error': 'Ingredient not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            ingredient.name = data['name']
        
        # Update allergen tags if provided
        if 'allergen_tags' in data:
            IngredientAllergenTag.query.filter_by(ingredient_id=ingredient_id).delete()
            for tag in data['allergen_tags']:
                allergen = IngredientAllergenTag(
                    ingredient_id=ingredient_id,
                    tag=tag
                )
                db.session.add(allergen)
        
        db.session.commit()
        
        return jsonify(ingredient.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dishes_bp.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """Delete an ingredient."""
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        
        if not ingredient:
            return jsonify({'error': 'Ingredient not found'}), 404
        
        db.session.delete(ingredient)
        db.session.commit()
        
        return jsonify({'message': 'Ingredient deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
