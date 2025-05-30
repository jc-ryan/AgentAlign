import json
from datetime import datetime, timedelta
import random
import uuid


def search_products_amazon(
    keyword: str,
    category: str = None,
    prime_only: bool = False,
    min_rating: float = None,
    price_range: tuple = None,
    sort_by: str = "relevance",
    filters: dict = None,
    page: int = 1,
    page_size: int = 20
) -> dict:
    """
    Search for products on Amazon
    Args:
        keyword: Search keyword
        category: Product category
        prime_only: Show only Prime-eligible items
        min_rating: Minimum rating (1-5)
        price_range: Tuple of (min_price, max_price)
        sort_by: Sort method (relevance/price_asc/price_desc/rating/reviews)
        filters: Additional filters (brand, condition, shipping_speed, etc.)
        page: Page number
        page_size: Items per page
    """
    if not keyword:
        return {
            "success": False,
            "error": "Missing required parameter: keyword"
        }

    filters = filters or {}
    
    # Generate mock search results
    results = []
    total_count = random.randint(100, 1000)
    
    for _ in range(min(page_size, total_count - (page-1)*page_size)):
        is_prime = random.choice([True, False])
        has_prime_delivery = is_prime and random.choice([True, False])
        
        product = {
            "id": f"amz_{uuid.uuid4().hex[:8]}",
            "title": f"Amazon Product {random.randint(1000, 9999)}",
            "price": round(random.uniform(10, 1000), 2),
            "rating": {
                "score": round(random.uniform(3.5, 5.0), 1),
                "count": random.randint(10, 10000)
            },
            "prime_eligible": is_prime,
            "delivery": {
                "prime_delivery": has_prime_delivery,
                "free_delivery": has_prime_delivery or random.choice([True, False]),
                "estimated_days": random.randint(1, 7)
            },
            "seller": {
                "name": "Amazon" if random.choice([True, False]) else f"Seller {random.randint(1000, 9999)}",
                "rating": round(random.uniform(90, 100), 1)
            },
            "badges": random.sample(
                ["Amazon's Choice", "Best Seller", "Limited Time Deal", "Climate Pledge Friendly"],
                k=random.randint(0, 2)
            ),
            "available_quantity": random.randint(0, 1000)
        }
        results.append(product)

    return {
        "success": True,
        "total_results": total_count,
        "page": page,
        "page_size": page_size,
        "results": results,
        "applied_filters": {
            "prime_only": prime_only,
            "min_rating": min_rating,
            "price_range": price_range,
            "category": category,
            "additional_filters": filters
        }
    }

def search_products_temu(
    query: str,
    category_id: str = None,
    sort_by: str = "recommended",
    min_price: float = None,
    max_price: float = None,
    shipping_region: str = "US",
    free_shipping: bool = False,
    page: int = 1
) -> dict:
    """
    Search for products on Temu
    Args:
        query: Search query
        category_id: Category ID
        sort_by: Sort method (recommended/price_low/price_high/orders/newest)
        min_price: Minimum price
        max_price: Maximum price
        shipping_region: Shipping region code
        free_shipping: Show only items with free shipping
        page: Page number
    """
    if not query:
        return {
            "success": False,
            "error": "Missing required parameter: query"
        }

    # Generate mock search results
    results = []
    total_pages = random.randint(10, 50)
    
    for _ in range(random.randint(20, 40)):
        original_price = round(random.uniform(20, 200), 2)
        discount = random.uniform(0.3, 0.8)
        product = {
            "id": f"temu_{uuid.uuid4().hex[:8]}",
            "title": f"Temu Product {random.randint(1000, 9999)}",
            "pricing": {
                "current_price": round(original_price * discount, 2),
                "original_price": original_price,
                "discount_percentage": round((1 - discount) * 100)
            },
            "shipping": {
                "is_free": random.choice([True, False]),
                "cost": 0 if free_shipping else round(random.uniform(2, 10), 2),
                "days_range": f"{random.randint(7, 10)}-{random.randint(15, 20)}"
            },
            "sales": {
                "total_orders": random.randint(100, 10000),
                "last_24h_orders": random.randint(10, 100)
            },
            "variants": {
                "total_options": random.randint(2, 10),
                "available_colors": random.randint(1, 5),
                "available_sizes": random.randint(1, 5)
            },
            "rating": {
                "score": round(random.uniform(4.0, 5.0), 1),
                "count": random.randint(50, 5000)
            },
            "flash_deal": random.choice([None, {
                "ends_in": random.randint(1, 24),
                "extra_discount": random.randint(5, 20)
            }])
        }
        results.append(product)

    return {
        "success": True,
        "results": results,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "has_next": page < total_pages
        },
        "search_metadata": {
            "category_id": category_id,
            "sort_by": sort_by,
            "price_range": {"min": min_price, "max": max_price},
            "shipping_region": shipping_region
        }
    }

def search_products_ebay(
    search_term: str,
    category: str = None,
    condition: list = None,
    min_price: float = None,
    max_price: float = None,
    buy_format: list = None,
    location: str = None,
    free_shipping: bool = False,
    best_offer: bool = False,
    returns_accepted: bool = False,
    page_number: int = 1
) -> dict:
    """
    Search for products on eBay
    Args:
        search_term: Search term
        category: Item category
        condition: List of conditions (new/used/not_specified)
        min_price: Minimum price
        max_price: Maximum price
        buy_format: List of formats (auction/buy_it_now/best_offer)
        location: Item location
        free_shipping: Show only items with free shipping
        best_offer: Show only items accepting Best Offer
        returns_accepted: Show only items with returns accepted
        page_number: Page number
    """
    if not search_term:
        return {
            "success": False,
            "error": "Missing required parameter: search_term"
        }

    # Generate mock search results
    results = []
    total_pages = random.randint(5, 50)
    
    for _ in range(random.randint(25, 50)):
        is_auction = random.choice([True, False])
        has_best_offer = not is_auction and random.choice([True, False])
        
        product = {
            "id": f"ebay_{uuid.uuid4().hex[:8]}",
            "title": f"eBay Item {random.randint(1000, 9999)}",
            "listing_info": {
                "format": "Auction" if is_auction else "Buy It Now",
                "condition": random.choice(["New", "Used", "Refurbished", "For parts or not working"]),
                "time_left": f"{random.randint(1, 24)}h {random.randint(0, 59)}m" if is_auction else "N/A"
            },
            "price": {
                "current_price": round(random.uniform(10, 1000), 2),
                "shipping_cost": 0 if free_shipping else round(random.uniform(3, 15), 2),
                "was_price": round(random.uniform(50, 2000), 2) if random.choice([True, False]) else None
            },
            "auction_info": {
                "bid_count": random.randint(0, 50) if is_auction else None,
                "best_offer_enabled": has_best_offer
            },
            "seller": {
                "name": f"seller_{random.randint(1000, 9999)}",
                "feedback_score": random.randint(50, 10000),
                "positive_feedback": round(random.uniform(90, 100), 1)
            },
            "item_location": f"City {random.randint(1, 100)}, Country",
            "shipping": {
                "type": random.choice(["Standard", "Expedited", "Economy"]),
                "free": free_shipping,
                "returns_accepted": random.choice([True, False])
            }
        }
        results.append(product)

    return {
        "success": True,
        "results": results,
        "pagination": {
            "current_page": page_number,
            "total_pages": total_pages,
            "items_per_page": len(results)
        },
        "filters": {
            "condition": condition,
            "price_range": {"min": min_price, "max": max_price},
            "buy_format": buy_format,
            "location": location,
            "shipping_options": {
                "free_shipping": free_shipping,
                "best_offer": best_offer,
                "returns_accepted": returns_accepted
            }
        }
    }

def search_products_taobao(
    keyword: str,
    cat: str = None,
    sort: str = "default",
    price_range: tuple = None,
    location: str = None,
    delivery_time: int = None,
    tmall_only: bool = False,
    has_coupon: bool = False,
    page: int = 1,
    page_size: int = 20
) -> dict:
    """
    Search for products on Taobao
    Args:
        keyword: Search keyword
        cat: Category ID
        sort: Sort method (default/sales/price_asc/price_desc/credit)
        price_range: Tuple of (min_price, max_price)
        location: Item location (province/city)
        delivery_time: Maximum delivery time in days
        tmall_only: Show only Tmall items
        has_coupon: Show only items with coupons
        page: Page number
        page_size: Items per page
    """
    if not keyword:
        return {
            "success": False,
            "error": "Missing required parameter: keyword"
        }

    # Generate mock search results
    results = []
    total_count = random.randint(1000, 10000)
    
    for _ in range(min(page_size, total_count - (page-1)*page_size)):
        is_tmall = random.choice([True, False])
        product = {
            "id": f"tb_{uuid.uuid4().hex[:8]}",
            "title": f"淘宝商品 {random.randint(1000, 9999)}",
            "price_info": {
                "current_price": round(random.uniform(10, 1000), 2),
                "original_price": round(random.uniform(20, 1200), 2),
                "lowest_price_in_30d": round(random.uniform(8, 900), 2)
            },
            "shop_info": {
                "name": f"{'天猫店铺' if is_tmall else '淘宝店铺'}_{random.randint(1000, 9999)}",
                "type": "tmall" if is_tmall else "taobao",
                "rating": {
                    "logistics": round(random.uniform(4.5, 5.0), 1),
                    "item_match": round(random.uniform(4.5, 5.0), 1),
                    "service": round(random.uniform(4.5, 5.0), 1)
                },
                "seller_level": random.randint(1, 20)
            },
            "item_info": {
                "sales_30d": random.randint(0, 10000),
                "comments_count": random.randint(0, 5000),
                "favorite_count": random.randint(0, 2000)
            },
            "promotion": {
                "has_coupon": random.choice([True, False]),
                "discount_value": random.randint(5, 50) if random.choice([True, False]) else None,
                "member_price": random.choice([True, False])
            },
            "shipping": {
                "location": random.choice(["广东省", "浙江省", "江苏省"]),
                "delivery_time": f"{random.randint(1, 3)}-{random.randint(4, 7)}天",
                "shipping_fee": round(random.uniform(0, 15), 2)
            }
        }
        results.append(product)

    return {
        "success": True,
        "total_count": total_count,
        "page_info": {
            "current_page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size
        },
        "results": results,
        "filters_applied": {
            "category": cat,
            "sort_method": sort,
            "price_range": price_range,
            "location": location,
            "delivery_time_limit": delivery_time,
            "tmall_only": tmall_only,
            "has_coupon": has_coupon
        }
    }

def place_order_amazon(
    item_id: str,
    quantity: int,
    shipping_address: str,
    shipping_method: str = "standard",
    gift: bool = False,
    gift_message: str = None,
    prime: bool = False
) -> dict:
    """
    Place an order on Amazon
    Args:
        item_id: Product ID
        quantity: Number of items to order
        shipping_address: Delivery address
        shipping_method: Shipping method (standard/expedited/prime)
        gift: Whether this is a gift
        gift_message: Optional gift message
        prime: Whether the user has Prime membership
    """
    if not all([item_id, quantity, shipping_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide item_id, quantity, and shipping_address."
        }
    
    if quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than 0"
        }

    # Generate random price and shipping fee
    unit_price = round(random.uniform(10, 1000), 2)
    shipping_fee = 0 if prime and shipping_method == "prime" else round(random.uniform(5, 20), 2)
    
    # Calculate estimated delivery date
    delivery_days = {
        "standard": random.randint(3, 7),
        "expedited": random.randint(1, 3),
        "prime": 2 if prime else random.randint(3, 7)
    }
    delivery_date = (datetime.now() + timedelta(days=delivery_days[shipping_method])).strftime("%Y-%m-%d")

    return {
        "success": True,
        "order_id": f"amz-{uuid.uuid4().hex[:8]}",
        "total_amount": round(unit_price * quantity + shipping_fee, 2),
        "breakdown": {
            "items_subtotal": round(unit_price * quantity, 2),
            "shipping_fee": shipping_fee
        },
        "estimated_delivery": delivery_date,
        "shipping_method": shipping_method,
        "is_prime_delivery": prime and shipping_method == "prime",
        "gift_info": {
            "is_gift": gift,
            "gift_message": gift_message if gift else None
        }
    }

def place_order_temu(
    item_id: str,
    quantity: int,
    shipping_address: str,
    color: str = None,
    size: str = None,
    insurance: bool = False
) -> dict:
    """
    Place an order on Temu
    Args:
        item_id: Product ID
        quantity: Number of items to order
        shipping_address: Delivery address
        color: Product color variant
        size: Product size variant
        insurance: Whether to add shipping insurance
    """
    if not all([item_id, quantity, shipping_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide item_id, quantity, and shipping_address."
        }

    if quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than 0"
        }

    # Generate random price and fees
    unit_price = round(random.uniform(1, 100), 2)
    shipping_fee = round(random.uniform(2, 10), 2)
    insurance_fee = 0.99 if insurance else 0

    return {
        "success": True,
        "order_id": f"temu-{uuid.uuid4().hex[:8]}",
        "total_amount": round(unit_price * quantity + shipping_fee + insurance_fee, 2),
        "breakdown": {
            "items_subtotal": round(unit_price * quantity, 2),
            "shipping_fee": shipping_fee,
            "insurance_fee": insurance_fee
        },
        "estimated_delivery": (datetime.now() + timedelta(days=random.randint(10, 20))).strftime("%Y-%m-%d"),
        "product_details": {
            "color": color,
            "size": size
        },
        "insurance_protected": insurance,
        "logistics_provider": random.choice(["USPS", "FedEx", "UPS"])
    }

def place_order_ebay(
    item_id: str,
    quantity: int,
    shipping_address: str,
    offer_price: float = None,
    shipping_option: str = "standard",
    payment_method: str = "paypal"
) -> dict:
    """
    Place an order on eBay
    Args:
        item_id: Product ID
        quantity: Number of items to order
        shipping_address: Delivery address
        offer_price: Price offered for negotiation (for items with "Best Offer" option)
        shipping_option: Shipping option (standard/expedited)
        payment_method: Payment method (paypal/card)
    """
    if not all([item_id, quantity, shipping_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide item_id, quantity, and shipping_address."
        }

    if quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than 0"
        }

    # Simulate if item allows best offer
    allows_best_offer = random.choice([True, False])
    if offer_price and not allows_best_offer:
        return {
            "success": False,
            "error": "This item does not accept Best Offers"
        }

    # Generate random price and fees
    list_price = round(random.uniform(10, 500), 2)
    final_price = offer_price if offer_price and offer_price <= list_price else list_price
    shipping_cost = round(random.uniform(3, 15), 2)

    return {
        "success": True,
        "order_id": f"ebay-{uuid.uuid4().hex[:8]}",
        "total_amount": round(final_price * quantity + shipping_cost, 2),
        "breakdown": {
            "items_subtotal": round(final_price * quantity, 2),
            "shipping_cost": shipping_cost
        },
        "payment_info": {
            "method": payment_method,
            "best_offer_accepted": True if offer_price and offer_price <= list_price else False
        },
        "shipping": {
            "method": shipping_option,
            "estimated_delivery": (datetime.now() + timedelta(days=random.randint(3, 10))).strftime("%Y-%m-%d"),
            "provider": random.choice(["USPS", "FedEx", "UPS"])
        },
        "seller_info": {
            "id": f"seller_{random.randint(1000, 9999)}",
            "rating": round(random.uniform(4.0, 5.0), 1)
        }
    }

def place_order_taobao(
    item_id: str,
    quantity: int,
    shipping_address: str,
    color_size: str = None,
    delivery_option: str = "standard",
    message_to_seller: str = None,
    use_points: bool = False
) -> dict:
    """
    Place an order on Taobao
    Args:
        item_id: Product ID
        quantity: Number of items to order
        shipping_address: Delivery address
        color_size: Combined color and size selection (e.g., "Red,XL")
        delivery_option: Delivery option (standard/express)
        message_to_seller: Optional message to seller
        use_points: Whether to use Taobao points for discount
    """
    if not all([item_id, quantity, shipping_address]):
        return {
            "success": False,
            "error": "Missing required parameters. Please provide item_id, quantity, and shipping_address."
        }

    if quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than 0"
        }

    # Generate random prices and points
    unit_price = round(random.uniform(10, 1000), 2)
    shipping_fee = round(random.uniform(5, 20), 2)
    available_points = random.randint(100, 1000)
    points_discount = round(min(available_points * 0.01, unit_price * quantity * 0.1), 2) if use_points else 0

    return {
        "success": True,
        "order_id": f"tb-{uuid.uuid4().hex[:8]}",
        "total_amount": round(unit_price * quantity + shipping_fee - points_discount, 2),
        "breakdown": {
            "items_subtotal": round(unit_price * quantity, 2),
            "shipping_fee": shipping_fee,
            "points_discount": points_discount
        },
        "product_details": {
            "color_size": color_size,
            "quantity": quantity
        },
        "shipping_info": {
            "method": delivery_option,
            "estimated_delivery": (datetime.now() + timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d"),
            "tracking_company": random.choice(["中通快递", "圆通快递", "顺丰快递"])
        },
        "seller_info": {
            "shop_name": f"Shop_{random.randint(1000, 9999)}",
            "wangwang_id": f"tb_{random.randint(10000, 99999)}"
        },
        "points_info": {
            "points_used": available_points if use_points else 0,
            "points_discount": points_discount
        },
        "message_to_seller": message_to_seller
    }