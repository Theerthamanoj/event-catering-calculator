from flask import Blueprint, jsonify
from models import Event
from calculator import calculate_portions

calculate_bp = Blueprint('calculate', __name__, url_prefix='/api')


@calculate_bp.route('/events/<int:event_id>/calculate', methods=['GET'])
def calculate_event(event_id):
    """
    Run catering calculation for an event.
    
    Returns cost matrix, dish quantities, and dietary conflict flags.
    """
    try:
        event = Event.query.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        if not event.guests or not event.menu_items:
            return jsonify({
                'error': 'Event must have guests and menu items to calculate',
                'event_id': event_id,
                'guest_count': len(event.guests),
                'menu_count': len(event.menu_items),
            }), 400
        
        result = calculate_portions(event, include_details=True)
        
        return jsonify({
            'event_id': event_id,
            'event_name': event.name,
            'result': result,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
