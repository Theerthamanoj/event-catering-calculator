from flask import Blueprint, request, jsonify
from models import db, Event, EventMenu, Dish
from sqlalchemy.exc import SQLAlchemyError

menu_bp = Blueprint('menu', __name__, url_prefix='/api')


@menu_bp.route('/events/<int:event_id>/menu', methods=['GET'])
def get_event_menu(event_id):
    """Get menu items for an event."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        menu_items = EventMenu.query.filter_by(event_id=event_id).all()
        return jsonify([item.to_dict() for item in menu_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@menu_bp.route('/events/<int:event_id>/menu', methods=['POST'])
def add_dish_to_menu(event_id):
    """Add a dish to event menu."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        data = request.get_json()
        
        if not data or 'dish_id' not in data:
            return jsonify({'error': 'dish_id is required'}), 400
        
        dish_id = data['dish_id']
        
        # Check if dish exists
        dish = Dish.query.get(dish_id)
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        # Check if already in menu
        existing = EventMenu.query.filter_by(
            event_id=event_id,
            dish_id=dish_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Dish already in menu'}), 409
        
        menu_item = EventMenu(
            event_id=event_id,
            dish_id=dish_id
        )
        
        db.session.add(menu_item)
        db.session.commit()
        
        return jsonify(menu_item.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@menu_bp.route('/events/<int:event_id>/menu/<int:dish_id>', methods=['DELETE'])
def remove_dish_from_menu(event_id, dish_id):
    """Remove a dish from event menu."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        menu_item = EventMenu.query.filter_by(
            event_id=event_id,
            dish_id=dish_id
        ).first()
        
        if not menu_item:
            return jsonify({'error': 'Menu item not found'}), 404
        
        db.session.delete(menu_item)
        db.session.commit()
        
        return jsonify({'message': 'Menu item removed'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
