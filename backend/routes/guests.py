from flask import Blueprint, request, jsonify
from models import db, Guest, GuestDietaryTag, Event
from sqlalchemy.exc import SQLAlchemyError

guests_bp = Blueprint('guests', __name__, url_prefix='/api')


@guests_bp.route('/events/<int:event_id>/guests', methods=['GET'])
def list_guests(event_id):
    """Get all guests for an event."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        guests = Guest.query.filter_by(event_id=event_id).all()
        return jsonify([guest.to_dict() for guest in guests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@guests_bp.route('/events/<int:event_id>/guests', methods=['POST'])
def create_guest(event_id):
    """Add a guest to an event."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        guest = Guest(
            event_id=event_id,
            name=data['name']
        )
        
        db.session.add(guest)
        db.session.flush()  # Get the guest ID
        
        # Add dietary tags
        tags = data.get('tags', [])
        for tag in tags:
            dietary_tag = GuestDietaryTag(guest_id=guest.id, tag=tag)
            db.session.add(dietary_tag)
        
        db.session.commit()
        
        return jsonify(guest.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@guests_bp.route('/guests/<int:guest_id>', methods=['GET'])
def get_guest(guest_id):
    """Get guest by ID."""
    try:
        guest = Guest.query.get(guest_id)
        
        if not guest:
            return jsonify({'error': 'Guest not found'}), 404
        
        return jsonify(guest.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@guests_bp.route('/guests/<int:guest_id>', methods=['PUT'])
def update_guest(guest_id):
    """Update a guest."""
    try:
        guest = Guest.query.get(guest_id)
        
        if not guest:
            return jsonify({'error': 'Guest not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            guest.name = data['name']
        
        # Update dietary tags if provided
        if 'tags' in data:
            # Delete old tags
            GuestDietaryTag.query.filter_by(guest_id=guest_id).delete()
            
            # Add new tags
            for tag in data['tags']:
                dietary_tag = GuestDietaryTag(guest_id=guest_id, tag=tag)
                db.session.add(dietary_tag)
        
        db.session.commit()
        
        return jsonify(guest.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@guests_bp.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    """Delete a guest."""
    try:
        guest = Guest.query.get(guest_id)
        
        if not guest:
            return jsonify({'error': 'Guest not found'}), 404
        
        db.session.delete(guest)
        db.session.commit()
        
        return jsonify({'message': 'Guest deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
