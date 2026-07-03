"""
Core catering calculation engine using set-intersection for dietary conflicts.
"""

ALLERGEN_CONFLICT_MAP = {
    'vegetarian': {'meat'},
    'vegan': {'meat', 'dairy', 'eggs', 'honey'},
    'gluten-free': {'gluten'},
    'gluten_free': {'gluten'},
    'nut allergy': {'nuts'},
    'nut_allergy': {'nuts'},
}


def get_forbidden_ingredients_for_guest(guest_tags):
    """
    Get union of all forbidden ingredient tags for a guest's dietary restrictions.
    
    Args:
        guest_tags: List of dietary restriction strings (e.g., ['vegetarian', 'gluten-free'])
    
    Returns:
        Set of forbidden ingredient tags
    """
    forbidden = set()
    for tag in guest_tags:
        forbidden.update(ALLERGEN_CONFLICT_MAP.get(tag, set()))
    return forbidden


def has_conflict(guest_tags, dish_allergens):
    """
    Check if a dish conflicts with a guest's dietary restrictions.
    Uses set intersection: forbidden_ingredients ∩ dish_allergens.
    
    Args:
        guest_tags: List of guest's dietary restriction tags
        dish_allergens: List of allergen tags in the dish
    
    Returns:
        Boolean: True if conflict exists, False otherwise
    """
    forbidden = get_forbidden_ingredients_for_guest(guest_tags)
    dish_allergen_set = set(dish_allergens)
    return bool(forbidden & dish_allergen_set)


def calculate_portions(event, include_details=False):
    """
    Calculate dish portions based on guest dietary restrictions and available menu.
    
    Args:
        event: Event object with guests and menu_items
        include_details: If True, include per-guest conflict details
    
    Returns:
        Dictionary with:
        - dishes: List of dish quantities and costs
        - cost_matrix: Cost breakdown by dietary group and dish
        - flagged_groups: Conflict warnings
    """
    from models import Guest, Dish
    
    guests = event.guests
    menu_dishes = [em.dish for em in event.menu_items]
    
    if not guests or not menu_dishes:
        return {
            'dishes': [],
            'cost_matrix': {
                'by_dietary_group': {},
                'by_dish': [],
                'grand_total': 0.0,
            },
            'flagged_groups': [],
        }
    
    # Calculate compatible portions per dish
    dish_data = []
    cost_by_dietary_group = {}
    grand_total = 0.0
    flagged_groups = []
    
    for dish in menu_dishes:
        dish_allergens = list(set([tag.tag for di in dish.ingredients for tag in di.ingredient.allergen_tags]))
        
        compatible_guests = []
        conflicted_guests_by_tag = {}
        
        for guest in guests:
            guest_tags = [tag.tag for tag in guest.dietary_tags]
            
            if has_conflict(guest_tags, dish_allergens):
                for tag in guest_tags:
                    if tag not in conflicted_guests_by_tag:
                        conflicted_guests_by_tag[tag] = []
                    conflicted_guests_by_tag[tag].append(guest.id)
            else:
                compatible_guests.append(guest.id)
        
        quantity = len(compatible_guests)
        total_cost = quantity * dish.per_head_cost
        grand_total += total_cost
        
        # Track flags
        flags = []
        for tag, affected_ids in conflicted_guests_by_tag.items():
            flags.append({
                'restriction': tag,
                'affected_guests': len(affected_ids),
            })
            if tag not in cost_by_dietary_group:
                cost_by_dietary_group[tag] = 0.0
        
        dish_entry = {
            'dish_id': dish.id,
            'name': dish.name,
            'quantity': quantity,
            'total_cost': round(total_cost, 2),
            'flagged_groups': flags,
        }
        
        if include_details:
            dish_entry['compatible_guest_count'] = len(compatible_guests)
            dish_entry['conflicted_count'] = len(guests) - len(compatible_guests)
        
        dish_data.append(dish_entry)
        
        # Add compatible guests' cost to their dietary groups
        for guest_id in compatible_guests:
            guest = next((g for g in guests if g.id == guest_id), None)
            if guest:
                for tag in [t.tag for t in guest.dietary_tags]:
                    if tag not in cost_by_dietary_group:
                        cost_by_dietary_group[tag] = 0.0
                    cost_by_dietary_group[tag] += dish.per_head_cost
    
    # Build cost matrix
    by_dish_breakdown = []
    for dish in menu_dishes:
        by_dish_breakdown.append({
            'dish': dish.name,
            'cost': dish.per_head_cost,
            'quantity': next((d['quantity'] for d in dish_data if d['dish_id'] == dish.id), 0),
        })
    
    return {
        'dishes': dish_data,
        'cost_matrix': {
            'by_dietary_group': {k: round(v, 2) for k, v in cost_by_dietary_group.items()},
            'by_dish': by_dish_breakdown,
            'grand_total': round(grand_total, 2),
        },
        'flagged_groups': flagged_groups,
    }
