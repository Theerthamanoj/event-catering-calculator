from flask import Blueprint, request, jsonify
from models import db, Event
from sqlalchemy.exc import SQLAlchemyError

events_bp = Blueprint('events', __name__, url_prefix='/api/events')


@events_bp.route('', methods=['GET'])
def list_events():
    """Get all events."""
    try:
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@events_bp.route('', methods=['POST'])
def create_event():
    """Create a new event."""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        event = Event(
            name=data['name'],
            date=data.get('date', ''),
            description=data.get('description', '')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify(event.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get event by ID."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        return jsonify(event.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            event.name = data['name']
        if 'date' in data:
            event.date = data['date']
        if 'description' in data:
            event.description = data['description']
        
        db.session.commit()
        
        return jsonify(event.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event."""
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'message': 'Event deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
