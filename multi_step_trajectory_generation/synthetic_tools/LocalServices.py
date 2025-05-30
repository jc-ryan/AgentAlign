import json
from datetime import datetime, timedelta
import random
import uuid


def search_merchant_meituan(
    keyword: str,
    location: str,
    sort_by: str = "comprehensive",
    filters: dict = None,
    page: int = 1,
    page_size: int = 20
) -> dict:
    """
    Search for merchants/stores on Meituan (restaurants, grocery stores, pharmacies, etc.)
    Args:
        keyword: Search keyword
        location: User's location
        sort_by: Sort method (comprehensive/distance/rating/sales)
        filters: Dict of filters (price_range, cuisine_type, delivery_time, etc.)
        page: Page number
        page_size: Items per page
    """
    if not all([keyword, location]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide keyword and location."
        }
    
    if sort_by not in ["comprehensive", "distance", "rating", "sales"]:
        return {
            "success": False,
            "error": "Invalid sort_by parameter. Must be one of: comprehensive, distance, rating, sales"
        }

    filters = filters or {}
    
    # Generate mock search results
    results = []
    total_count = random.randint(50, 200)
    for _ in range(min(page_size, total_count - (page-1)*page_size)):
        restaurant = {
            "id": f"mt_rest_{uuid.uuid4().hex[:8]}",
            "name": random.choice(["川味小馆", "粤式茶餐厅", "寿司屋", "麻辣烫", "沙县小吃"]),
            "rating": round(random.uniform(4.0, 4.9), 1),
            "monthly_sales": random.randint(500, 5000),
            "average_price": random.randint(15, 80),
            "delivery_time": f"{random.randint(20, 60)}分钟",
            "distance": round(random.uniform(0.1, 5.0), 1),
            "delivery_fee": round(random.uniform(3, 10), 2),
            "promotion": random.choice([None, "满30减5", "新店立减10元", None]),
            "is_premium_merchant": random.choice([True, False]),
            "categories": random.sample(["中餐", "日料", "快餐", "面食", "火锅"], random.randint(1, 3))
        }
        results.append(restaurant)

    return {
        "success": True,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "location": location,
        "results": results,
        "applied_filters": filters,
        "sort_method": sort_by
    }

def search_merchant_doordash(
    query: str,
    address: str,
    cuisine_type: str = None,
    price_range: str = None,
    dietary_preferences: list = None,
    rating_min: float = None,
    delivery_time_max: int = None,
    top_rated_only: bool = False
) -> dict:
    """
    Search for merchants on DoorDash (restaurants, convenience stores, retail shops, etc.)
    Args:
        query: Search query
        address: Delivery address
        cuisine_type: Type of cuisine
        price_range: Price range ($, $$, $$$)
        dietary_preferences: List of dietary preferences (vegetarian, vegan, gluten-free)
        rating_min: Minimum rating (1-5)
        delivery_time_max: Maximum delivery time in minutes
        top_rated_only: Show only top-rated restaurants
    """
    if not all([query, address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide query and address."
        }

    if price_range and price_range not in ["$", "$$", "$$$"]:
        return {
            "success": False,
            "error": "Invalid price_range. Must be one of: $, $$, $$$"
        }

    # Generate mock search results
    results = []
    result_count = random.randint(5, 25)
    
    for _ in range(result_count):
        restaurant = {
            "id": f"dd_rest_{uuid.uuid4().hex[:8]}",
            "name": random.choice(["Burger Joint", "Pizza Palace", "Taco Town", "Sushi Spot", "Salad Bar"]),
            "rating": round(random.uniform(3.8, 4.9), 1),
            "rating_count": random.randint(50, 1000),
            "price_level": random.choice(["$", "$$", "$$$"]),
            "estimated_delivery_time": f"{random.randint(20, 50)} min",
            "delivery_fee": f"${round(random.uniform(0.99, 7.99), 2)}",
            "distance_miles": round(random.uniform(0.1, 8.0), 1),
            "is_dashpass": random.choice([True, False]),
            "dietary_tags": random.sample(["Vegetarian", "Vegan", "Gluten-Free"], random.randint(0, 2)),
            "featured_items": [
                {"name": f"Item {i}", "price": round(random.uniform(8, 25), 2)}
                for i in range(random.randint(2, 4))
            ]
        }
        results.append(restaurant)

    return {
        "success": True,
        "results": results,
        "filters_applied": {
            "cuisine_type": cuisine_type,
            "price_range": price_range,
            "dietary_preferences": dietary_preferences,
            "rating_min": rating_min,
            "delivery_time_max": delivery_time_max,
            "top_rated_only": top_rated_only
        },
        "total_results": result_count,
        "delivery_address": address
    }

def search_merchant_ubereats(
    search_term: str,
    delivery_location: str,
    sort_by: str = "recommended",
    price_level: list = None,
    dietary_restrictions: list = None,
    max_delivery_fee: float = None,
    max_delivery_time: int = None
) -> dict:
    """
    Search for merchants on Uber Eats (restaurants, grocery stores, packaged goods, etc.)
    Args:
        search_term: Search term
        delivery_location: Delivery location
        sort_by: Sort method (recommended/rating/delivery_time/price)
        price_level: List of price levels (1-4)
        dietary_restrictions: List of dietary restrictions
        max_delivery_fee: Maximum delivery fee
        max_delivery_time: Maximum delivery time in minutes
    """
    if not all([search_term, delivery_location]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide search_term and delivery_location."
        }

    if sort_by not in ["recommended", "rating", "delivery_time", "price"]:
        return {
            "success": False,
            "error": "Invalid sort_by parameter"
        }

    # Generate mock search results
    results = []
    for _ in range(random.randint(8, 30)):
        restaurant = {
            "id": f"ue_rest_{uuid.uuid4().hex[:8]}",
            "name": random.choice(["The Grill House", "Fresh Fusion", "Noodle Bar", "Health Kitchen", "Street Eats"]),
            "rating": {
                "score": round(random.uniform(4.0, 4.9), 1),
                "count": random.randint(100, 2000)
            },
            "price_level": random.randint(1, 4),
            "delivery": {
                "estimate": f"{random.randint(10, 45)}-{random.randint(46, 60)} min",
                "fee": round(random.uniform(0, 4.99), 2)
            },
            "promotional_banner": random.choice([
                None,
                {"type": "DEAL", "text": "$0 Delivery Fee"},
                {"type": "DISCOUNT", "text": "20% Off Your Order"}
            ]),
            "badges": random.sample([
                "Popular", "Fast Delivery", "Top Rated", "New on Uber Eats"
            ], random.randint(0, 2)),
            "special_features": {
                "group_ordering": random.choice([True, False]),
                "scheduled_delivery": True
            }
        }
        results.append(restaurant)

    return {
        "success": True,
        "search_location": delivery_location,
        "results": results,
        "filters": {
            "sort_by": sort_by,
            "price_level": price_level,
            "dietary_restrictions": dietary_restrictions,
            "max_delivery_fee": max_delivery_fee,
            "max_delivery_time": max_delivery_time
        },
        "promotions": {
            "banner": "Free delivery on your first order!",
            "active_deals": random.randint(3, 8)
        }
    }

def search_merchant_foodpanda(
    search_text: str,
    area: str,
    cuisine: str = None,
    min_order_value: float = None,
    delivery_time: str = None,
    vouchers_only: bool = False,
    free_delivery: bool = False,
    page: int = 1
) -> dict:
    """
    Search for merchants on Foodpanda (restaurants, grocery stores, convenience stores, etc.)
    Args:
        search_text: Search text
        area: Delivery area
        cuisine: Cuisine type
        min_order_value: Minimum order value
        delivery_time: Preferred delivery time (YYYY-MM-DD HH:MM)
        vouchers_only: Show only restaurants with active vouchers
        free_delivery: Show only restaurants with free delivery
        page: Page number
    """
    if not all([search_text, area]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide search_text and area."
        }

    if delivery_time:
        try:
            datetime.strptime(delivery_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid delivery_time format. Use 'YYYY-MM-DD HH:MM'"
            }

    # Generate mock search results
    results = []
    total_pages = random.randint(3, 8)
    
    for _ in range(random.randint(10, 20)):
        restaurant = {
            "id": f"fp_rest_{uuid.uuid4().hex[:8]}",
            "name": random.choice([
                "Asian Kitchen", "Western Delights", "Local Favorites", 
                "Vegetarian Paradise", "Fast Food Express"
            ]),
            "rating": {
                "value": round(random.uniform(3.5, 4.8), 1),
                "count": random.randint(50, 500)
            },
            "delivery_info": {
                "time": f"{random.randint(25, 55)} min",
                "fee": round(random.uniform(0, 5), 2),
                "minimum_order": round(random.uniform(10, 25), 2)
            },
            "available_promos": random.sample([
                "10% off entire menu",
                "Free delivery",
                "Buy 1 Get 1 Free",
                "New customer discount"
            ], random.randint(0, 2)),
            "tags": random.sample([
                "Halal", "Vegetarian friendly", "Popular", "Partner Restaurant"
            ], random.randint(1, 3)),
            "operational_status": {
                "is_open": random.choice([True, False]),
                "next_open": "Tomorrow 10:00" if random.choice([True, False]) else None
            }
        }
        results.append(restaurant)

    return {
        "success": True,
        "results": results,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "has_next": page < total_pages
        },
        "search_filters": {
            "cuisine": cuisine,
            "min_order_value": min_order_value,
            "delivery_time": delivery_time,
            "vouchers_only": vouchers_only,
            "free_delivery": free_delivery
        },
        "area_info": {
            "name": area,
            "available_restaurants": random.randint(50, 200)
        }
    }

def place_order_meituan(
    restaurant_id: str,
    items: list,
    delivery_address: str,
    delivery_time: str = "now",
    cutlery_count: int = 1,
    note_to_restaurant: str = None,
    note_to_driver: str = None,
    contact_phone: str = None
) -> dict:
    """
    Place a food delivery order on Meituan
    Args:
        restaurant_id: ID of the restaurant
        items: List of items to order, each item should be dict with 'item_id', 'quantity', and optional 'notes'
        delivery_address: Delivery address
        delivery_time: Delivery time ("now" or future time)
        cutlery_count: Number of sets of cutlery
        note_to_restaurant: Special instructions for restaurant
        note_to_driver: Special instructions for delivery driver
        contact_phone: Contact phone number
    """
    if not all([restaurant_id, items, delivery_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide restaurant_id, items, and delivery_address."
        }

    if not isinstance(items, list) or not items:
        return {
            "success": False,
            "error": "Items must be a non-empty list of food items"
        }

    # Calculate prices and fees
    items_price = sum(random.uniform(10, 50) * item.get('quantity', 1) for item in items)
    delivery_fee = round(random.uniform(3, 10), 2)
    platform_fee = round(items_price * 0.05, 2)  # 5% platform fee

    # Handle delivery time
    if delivery_time == "now":
        estimated_time = datetime.now() + timedelta(minutes=random.randint(30, 60))
    else:
        try:
            estimated_time = datetime.strptime(delivery_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid delivery_time format. Use 'now' or 'YYYY-MM-DD HH:MM'"
            }

    return {
        "success": True,
        "order_id": f"mt-{uuid.uuid4().hex[:8]}",
        "total_amount": round(items_price + delivery_fee + platform_fee, 2),
        "breakdown": {
            "items_total": round(items_price, 2),
            "delivery_fee": delivery_fee,
            "platform_fee": platform_fee
        },
        "delivery_info": {
            "estimated_time": estimated_time.strftime("%Y-%m-%d %H:%M"),
            "delivery_address": delivery_address,
            "cutlery_count": cutlery_count
        },
        "notes": {
            "to_restaurant": note_to_restaurant,
            "to_driver": note_to_driver
        },
        "contact_phone": contact_phone,
        "status": "confirmed",
        "payment_method": "online"  # Meituan typically uses online payment
    }

def place_order_doordash(
    restaurant_id: str,
    items: list,
    delivery_address: str,
    tip_amount: float = 0,
    delivery_instructions: str = None,
    scheduled_time: str = None,
    no_contact_delivery: bool = True,
    priority_delivery: bool = False
) -> dict:
    """
    Place a food delivery order on DoorDash
    Args:
        restaurant_id: ID of the restaurant
        items: List of items to order, each item should be dict with 'item_id', 'quantity', and optional 'customizations'
        delivery_address: Delivery address
        tip_amount: Tip amount for the dasher
        delivery_instructions: Delivery instructions
        scheduled_time: Schedule delivery for later (YYYY-MM-DD HH:MM)
        no_contact_delivery: Whether to enable no-contact delivery
        priority_delivery: Whether to enable priority delivery
    """
    if not all([restaurant_id, items, delivery_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide restaurant_id, items, and delivery_address."
        }

    if not isinstance(items, list) or not items:
        return {
            "success": False,
            "error": "Items must be a non-empty list of food items"
        }

    # Calculate prices and fees
    subtotal = sum(random.uniform(8, 40) * item.get('quantity', 1) for item in items)
    delivery_fee = round(random.uniform(2.99, 7.99), 2)
    service_fee = round(subtotal * 0.15, 2)  # 15% service fee
    priority_fee = 2.99 if priority_delivery else 0
    
    # Calculate delivery time
    if scheduled_time:
        try:
            delivery_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid scheduled_time format. Use 'YYYY-MM-DD HH:MM'"
            }
    else:
        delivery_time = datetime.now() + timedelta(minutes=random.randint(25, 45))

    return {
        "success": True,
        "order_id": f"dd-{uuid.uuid4().hex[:8]}",
        "total_amount": round(subtotal + delivery_fee + service_fee + tip_amount + priority_fee, 2),
        "breakdown": {
            "subtotal": round(subtotal, 2),
            "delivery_fee": delivery_fee,
            "service_fee": service_fee,
            "dasher_tip": round(tip_amount, 2),
            "priority_fee": priority_fee
        },
        "delivery_details": {
            "estimated_time": delivery_time.strftime("%Y-%m-%d %H:%M"),
            "address": delivery_address,
            "instructions": delivery_instructions,
            "no_contact": no_contact_delivery,
            "priority": priority_delivery
        },
        "order_status": "confirmed",
        "dasher_status": "searching_for_dasher"
    }

def place_order_ubereats(
    restaurant_id: str,
    items: list,
    delivery_address: str,
    tip_percent: float = 15.0,
    delivery_notes: str = None,
    schedule_for: str = None,
    priority: bool = False,
    group_order: bool = False
) -> dict:
    """
    Place a food delivery order on Uber Eats
    Args:
        restaurant_id: ID of the restaurant
        items: List of items to order, each item should be dict with 'item_id', 'quantity', and optional 'special_instructions'
        delivery_address: Delivery address
        tip_percent: Tip percentage (0-30)
        delivery_notes: Delivery instructions
        schedule_for: Schedule delivery time (YYYY-MM-DD HH:MM)
        priority: Whether to enable priority delivery
        group_order: Whether this is a group order
    """
    if not all([restaurant_id, items, delivery_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide restaurant_id, items, and delivery_address."
        }

    if not isinstance(items, list) or not items:
        return {
            "success": False,
            "error": "Items must be a non-empty list of food items"
        }

    if not 0 <= tip_percent <= 30:
        return {
            "success": False,
            "error": "Tip percentage must be between 0 and 30"
        }

    # Calculate prices and fees
    subtotal = sum(random.uniform(10, 45) * item.get('quantity', 1) for item in items)
    delivery_fee = round(random.uniform(0.99, 5.99), 2)
    service_fee = round(subtotal * 0.15, 2)  # 15% service fee
    tip_amount = round(subtotal * (tip_percent / 100), 2)
    priority_fee = 1.99 if priority else 0

    # Handle delivery time
    if schedule_for:
        try:
            delivery_time = datetime.strptime(schedule_for, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid schedule_for format. Use 'YYYY-MM-DD HH:MM'"
            }
    else:
        delivery_time = datetime.now() + timedelta(minutes=random.randint(30, 50))

    return {
        "success": True,
        "order_id": f"ue-{uuid.uuid4().hex[:8]}",
        "total_amount": round(subtotal + delivery_fee + service_fee + tip_amount + priority_fee, 2),
        "breakdown": {
            "subtotal": round(subtotal, 2),
            "delivery_fee": delivery_fee,
            "service_fee": service_fee,
            "tip": tip_amount,
            "priority_fee": priority_fee
        },
        "delivery_info": {
            "estimated_time": delivery_time.strftime("%Y-%m-%d %H:%M"),
            "address": delivery_address,
            "notes": delivery_notes,
            "priority": priority
        },
        "group_order": {
            "is_group_order": group_order,
            "status": "closed" if not group_order else "collecting_orders"
        },
        "order_status": "confirmed",
        "courier_status": "matching_courier"
    }

def place_order_foodpanda(
    restaurant_id: str,
    items: list,
    delivery_address: str,
    voucher_code: str = None,
    remarks: str = None,
    schedule_time: str = None,
    payment_method: str = "card",
    pro_member: bool = False
) -> dict:
    """
    Place a food delivery order on Foodpanda
    Args:
        restaurant_id: ID of the restaurant
        items: List of items to order, each item should be dict with 'item_id', 'quantity', and optional 'add_ons'
        delivery_address: Delivery address
        voucher_code: Voucher code for discount
        remarks: Delivery remarks
        schedule_time: Schedule delivery time (YYYY-MM-DD HH:MM)
        payment_method: Payment method (card/cash)
        pro_member: Whether user is a pro member
    """
    if not all([restaurant_id, items, delivery_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide restaurant_id, items, and delivery_address."
        }

    if not isinstance(items, list) or not items:
        return {
            "success": False,
            "error": "Items must be a non-empty list of food items"
        }

    if payment_method not in ["card", "cash"]:
        return {
            "success": False,
            "error": "Invalid payment method. Use 'card' or 'cash'"
        }

    # Calculate prices and fees
    subtotal = sum(random.uniform(5, 35) * item.get('quantity', 1) for item in items)
    delivery_fee = 0 if pro_member else round(random.uniform(2, 8), 2)
    service_fee = round(subtotal * 0.10, 2)  # 10% service fee

    # Apply voucher if provided
    discount = 0
    if voucher_code:
        discount = round(min(random.uniform(5, 15), subtotal * 0.3), 2)  # Max 30% discount

    # Handle delivery time
    if schedule_time:
        try:
            delivery_time = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid schedule_time format. Use 'YYYY-MM-DD HH:MM'"
            }
    else:
        delivery_time = datetime.now() + timedelta(minutes=random.randint(35, 55))

    return {
        "success": True,
        "order_id": f"fp-{uuid.uuid4().hex[:8]}",
        "total_amount": round(subtotal + delivery_fee + service_fee - discount, 2),
        "breakdown": {
            "subtotal": round(subtotal, 2),
            "delivery_fee": delivery_fee,
            "service_fee": service_fee,
            "discount": discount,
            "voucher_applied": bool(voucher_code)
        },
        "delivery_info": {
            "estimated_time": delivery_time.strftime("%Y-%m-%d %H:%M"),
            "address": delivery_address,
            "remarks": remarks
        },
        "payment": {
            "method": payment_method,
            "status": "paid" if payment_method == "card" else "pending"
        },
        "membership": {
            "is_pro": pro_member,
            "benefits_applied": ["free_delivery"] if pro_member else []
        },
        "order_status": "confirmed",
        "restaurant_status": "preparing"
    }