# Backend - Event Catering Calculator API

Python Flask backend for the Event Catering Calculator application.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

The database is automatically created when the app starts. To seed with sample data:

```bash
python seed.py
```

This creates:
- 27 ingredients with allergen tags (meat, dairy, eggs, honey, gluten, nuts, fish)
- 7 dishes with ingredient combinations
- 2 sample events with 13 guests and mixed dietary restrictions

### 3. Run the Server

```bash
python app.py
```

Or with Flask CLI:

```bash
flask run
```

Server runs on `http://localhost:5000`

## API Endpoints

### Events

- `GET /api/events` - List all events
- `POST /api/events` - Create new event
- `GET /api/events/<id>` - Get event details
- `PUT /api/events/<id>` - Update event
- `DELETE /api/events/<id>` - Delete event

**Request body (POST/PUT):**
```json
{
  "name": "Event Name",
  "date": "Date string",
  "description": "Optional description"
}
```

### Guests

- `GET /api/events/<event_id>/guests` - List event guests
- `POST /api/events/<event_id>/guests` - Add guest to event
- `GET /api/guests/<id>` - Get guest details
- `PUT /api/guests/<id>` - Update guest
- `DELETE /api/guests/<id>` - Delete guest

**Request body (POST/PUT):**
```json
{
  "name": "Guest Name",
  "tags": ["vegetarian", "gluten-free"]
}
```

Available dietary tags: `vegetarian`, `vegan`, `gluten-free`, `nut-allergy`

### Dishes

- `GET /api/dishes` - List all dishes
- `POST /api/dishes` - Create new dish
- `GET /api/dishes/<id>` - Get dish details
- `PUT /api/dishes/<id>` - Update dish
- `DELETE /api/dishes/<id>` - Delete dish

**Request body (POST/PUT):**
```json
{
  "name": "Dish Name",
  "per_head_cost": 14.00,
  "category": "Signature",
  "description": "Dish description",
  "ingredients": [1, 2, 3]
}
```

### Ingredients

- `GET /api/ingredients` - List all ingredients
- `POST /api/ingredients` - Create ingredient
- `GET /api/ingredients/<id>` - Get ingredient details
- `PUT /api/ingredients/<id>` - Update ingredient
- `DELETE /api/ingredients/<id>` - Delete ingredient

**Request body (POST/PUT):**
```json
{
  "name": "Ingredient Name",
  "allergen_tags": ["gluten", "dairy"]
}
```

Available allergen tags: `meat`, `dairy`, `eggs`, `honey`, `gluten`, `nuts`, `fish`

### Event Menu

- `GET /api/events/<event_id>/menu` - Get event menu dishes
- `POST /api/events/<event_id>/menu` - Add dish to menu
- `DELETE /api/events/<event_id>/menu/<dish_id>` - Remove dish from menu

**Request body (POST):**
```json
{
  "dish_id": 1
}
```

### Calculation

- `GET /api/events/<event_id>/calculate` - Run catering calculation

**Response:**
```json
{
  "event_id": 1,
  "event_name": "Event Name",
  "result": {
    "dishes": [
      {
        "dish_id": 1,
        "name": "Dish Name",
        "quantity": 14,
        "total_cost": 196.00,
        "flagged_groups": [
          {
            "restriction": "gluten-free",
            "affected_guests": 3
          }
        ]
      }
    ],
    "cost_matrix": {
      "by_dietary_group": {
        "vegetarian": 320.00,
        "gluten-free": 180.00
      },
      "by_dish": [
        {
          "dish": "Dish Name",
          "cost": 14.00,
          "quantity": 14
        }
      ],
      "grand_total": 1240.00
    },
    "flagged_groups": []
  }
}
```

## Database Schema

### Tables

1. **events** - Event information
2. **guests** - Guests attending events
3. **guest_dietary_tags** - Dietary restrictions per guest
4. **dishes** - Dish recipes and costs
5. **ingredients** - Ingredient library
6. **ingredient_allergen_tags** - Allergen tags per ingredient
7. **dish_ingredients** - Ingredients in each dish
8. **event_menu** - Menu selection for each event

## Core Algorithm

The calculator uses **set intersection** to detect dietary conflicts:

1. For each guest, collect all forbidden ingredients based on their dietary tags
2. For each dish, collect all allergen tags from its ingredients
3. If `forbidden_ingredients ∩ dish_allergens` is not empty → conflict exists
4. Only compatible guests are counted for a dish portion

Example:
- Guest: `[vegetarian, gluten-free]`
- Forbidden: `{meat, gluten}`
- Dish: Pasta with meat (allergens: `[meat, gluten]`)
- Conflict: Yes (meat is forbidden)

## CORS

CORS is enabled for all origins in development. Configure in `app.py` for production.

## Database File

SQLite database is stored as `event_catering.db` in the backend directory.

## Error Handling

All endpoints return standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad request
- `404` - Not found
- `409` - Conflict (e.g., duplicate ingredient)
- `500` - Server error

Error responses include a JSON body with an `error` field:
```json
{
  "error": "Event not found"
}
```
