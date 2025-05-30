"""
Payment platform simulation functions.
This module provides mock implementations of payment functionalities
for various payment platforms including Alipay, Apple Pay, PayPal, and WeChat Pay.
"""

import time
import random
from typing import Optional, Dict, Any, Union, List
from decimal import Decimal

# Common utility functions
def generate_id(prefix: str = "") -> str:
    """Generates a unique ID with optional prefix."""
    return f"{prefix}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def validate_amount(amount: Union[float, str, Decimal]) -> Optional[Dict[str, str]]:
    """
    Validates payment amount.
    Returns error dict if invalid, None if valid.
    """
    try:
        amount_decimal = Decimal(str(amount))
        if amount_decimal <= 0:
            return {"error": "Amount must be greater than 0"}
        if amount_decimal.as_tuple().exponent < -2:
            return {"error": "Amount cannot have more than 2 decimal places"}
    except:
        return {"error": "Invalid amount format"}
    return None

def validate_currency(currency: str) -> Optional[Dict[str, str]]:
    """
    Validates currency code.
    Returns error dict if invalid, None if valid.
    """
    valid_currencies = {'USD', 'CNY', 'JPY', 'EUR', 'GBP', 'HKD', 'CAD', 'AUD'}
    if currency not in valid_currencies:
        return {"error": f"Unsupported currency. Must be one of: {', '.join(valid_currencies)}"}
    return None

# Alipay Functions
def create_alipay_payment(
    amount: Union[float, str],
    currency: str = "CNY",
    subject: str = "",
    buyer_id: Optional[str] = None,
    payment_method: str = "BALANCE",  # BALANCE, BANK_CARD, CREDIT_PAY
    notify_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Creates an Alipay payment request.
    
    Args:
        amount: Payment amount
        currency: Payment currency (default: CNY)
        subject: Payment subject/description
        buyer_id: Alipay user ID of the buyer
        payment_method: Payment method to use
        notify_url: URL for receiving payment notifications
    
    Returns:
        Dict containing payment details or error message
    """
    # Validate inputs
    if amount_error := validate_amount(amount):
        return amount_error
    if currency_error := validate_currency(currency):
        return currency_error
    if not subject:
        return {"error": "Payment subject is required"}
    
    valid_payment_methods = {'BALANCE', 'BANK_CARD', 'CREDIT_PAY'}
    if payment_method not in valid_payment_methods:
        return {"error": f"Invalid payment method. Must be one of: {', '.join(valid_payment_methods)}"}

    # Generate payment details
    payment_id = generate_id("alipay")
    qr_code = f"https://mock-qr.alipay.com/{payment_id}"  # Mock QR code URL
    
    response = {
        "payment_id": payment_id,
        "created_at": get_current_timestamp(),
        "amount": str(Decimal(str(amount)).quantize(Decimal('0.01'))),
        "currency": currency,
        "subject": subject,
        "payment_method": payment_method,
        "status": "CREATED",
        "qr_code": qr_code,
        "expire_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", 
                                   time.gmtime(time.time() + 3600))  # 1 hour expiry
    }
    
    if buyer_id:
        response["buyer_id"] = buyer_id
    if notify_url:
        response["notify_url"] = notify_url
        
    return response

def query_alipay_payment(payment_id: str) -> Dict[str, Any]:
    """
    Queries the status of an Alipay payment.
    
    Args:
        payment_id: The payment ID to query
    
    Returns:
        Dict containing payment status and details
    """
    if not payment_id:
        return {"error": "Payment ID is required"}
    
    # Simulate different payment states
    status_options = ['CREATED', 'PAID', 'FAILED', 'CLOSED']
    status = random.choice(status_options)
    
    response = {
        "payment_id": payment_id,
        "status": status,
        "query_time": get_current_timestamp()
    }
    
    if status == 'PAID':
        response.update({
            "paid_amount": "100.00",  # Mock amount
            "paid_at": get_current_timestamp(),
            "trade_no": generate_id("trade")
        })
    elif status == 'FAILED':
        response["error_code"] = "PAYMENT_FAILED"
        response["error_message"] = "Payment processing failed"
        
    return response

# Apple Pay Functions
def create_apple_pay_payment(
    amount: Union[float, str],
    currency: str = "USD",
    merchant_id: str = "",
    payment_data: Dict[str, Any] = None,
    line_items: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Creates an Apple Pay payment request.
    
    Args:
        amount: Payment amount
        currency: Payment currency (default: USD)
        merchant_id: Apple Pay merchant identifier
        payment_data: Encrypted payment data from Apple Pay
        line_items: List of items being purchased
    
    Returns:
        Dict containing payment details or error message
    """
    # Validate inputs
    if amount_error := validate_amount(amount):
        return amount_error
    if currency_error := validate_currency(currency):
        return currency_error
    if not merchant_id:
        return {"error": "Merchant ID is required"}
    if not payment_data:
        return {"error": "Payment data is required"}

    payment_id = generate_id("applepay")
    
    response = {
        "payment_id": payment_id,
        "created_at": get_current_timestamp(),
        "amount": str(Decimal(str(amount)).quantize(Decimal('0.01'))),
        "currency": currency,
        "merchant_id": merchant_id,
        "status": "PROCESSING",
        "payment_method": {
            "type": "APPLE_PAY",
            "network": payment_data.get("network", "VISA"),  # or MASTERCARD, AMEX, etc.
            "token_type": "APPLEPAY"
        }
    }
    
    if line_items:
        response["line_items"] = line_items
        
    return response

def query_apple_pay_payment(payment_id: str) -> Dict[str, Any]:
    """
    Queries the status of an Apple Pay payment.
    
    Args:
        payment_id: The payment ID to query
    
    Returns:
        Dict containing payment status and details
    """
    if not payment_id:
        return {"error": "Payment ID is required"}
    
    status_options = ['PROCESSING', 'COMPLETED', 'FAILED', 'DECLINED']
    status = random.choice(status_options)
    
    response = {
        "payment_id": payment_id,
        "status": status,
        "query_time": get_current_timestamp()
    }
    
    if status == 'COMPLETED':
        response.update({
            "transaction_id": generate_id("transaction"),
            "completed_at": get_current_timestamp()
        })
    elif status in ['FAILED', 'DECLINED']:
        response["decline_reason"] = random.choice([
            "INSUFFICIENT_FUNDS",
            "INVALID_CARD",
            "RISK_DECLINED",
            "EXPIRED_CARD"
        ])
        
    return response

# PayPal Functions
def create_paypal_payment(
    amount: Union[float, str],
    currency: str = "USD",
    description: str = "",
    intent: str = "CAPTURE",  # CAPTURE or AUTHORIZE
    payer_email: Optional[str] = None,
    return_url: Optional[str] = None,
    cancel_url: Optional[str] = None,
    items: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Creates a PayPal payment request.
    
    Args:
        amount: Payment amount
        currency: Payment currency (default: USD)
        description: Payment description
        intent: Payment intent (CAPTURE or AUTHORIZE)
        payer_email: Email of the payer
        return_url: Success return URL
        cancel_url: Cancel return URL
        items: List of items being purchased
    
    Returns:
        Dict containing payment details or error message
    """
    # Validate inputs
    if amount_error := validate_amount(amount):
        return amount_error
    if currency_error := validate_currency(currency):
        return currency_error
    if intent not in ['CAPTURE', 'AUTHORIZE']:
        return {"error": "Intent must be either CAPTURE or AUTHORIZE"}

    payment_id = generate_id("paypal")
    
    response = {
        "payment_id": payment_id,
        "created_at": get_current_timestamp(),
        "amount": {
            "total": str(Decimal(str(amount)).quantize(Decimal('0.01'))),
            "currency": currency
        },
        "intent": intent,
        "status": "CREATED",
        "links": [
            {
                "rel": "approve",
                "href": f"https://mock-paypal.com/approve/{payment_id}",
                "method": "GET"
            },
            {
                "rel": "capture",
                "href": f"https://mock-paypal.com/capture/{payment_id}",
                "method": "POST"
            }
        ]
    }
    
    if description:
        response["description"] = description
    if payer_email:
        response["payer"] = {"email_address": payer_email}
    if return_url:
        response["return_url"] = return_url
    if cancel_url:
        response["cancel_url"] = cancel_url
    if items:
        response["items"] = items
        
    return response

def query_paypal_payment(payment_id: str) -> Dict[str, Any]:
    """
    Queries the status of a PayPal payment.
    
    Args:
        payment_id: The payment ID to query
    
    Returns:
        Dict containing payment status and details
    """
    if not payment_id:
        return {"error": "Payment ID is required"}
    
    status_options = ['CREATED', 'APPROVED', 'COMPLETED', 'FAILED', 'VOIDED']
    status = random.choice(status_options)
    
    response = {
        "payment_id": payment_id,
        "status": status,
        "query_time": get_current_timestamp()
    }
    
    if status in ['APPROVED', 'COMPLETED']:
        response.update({
            "transaction_id": generate_id("transaction"),
            "payer": {
                "payer_id": generate_id("payer"),
                "country_code": "US"
            },
            "update_time": get_current_timestamp()
        })
    elif status == 'FAILED':
        response["error"] = {
            "name": "PAYMENT_FAILED",
            "message": "The payment failed to process",
            "debug_id": generate_id("debug")
        }
        
    return response

# WeChat Pay Functions
def create_wechat_pay_payment(
    amount: Union[float, str],
    currency: str = "CNY",
    description: str = "",
    trade_type: str = "NATIVE",  # NATIVE(QR), JSAPI(Mini Program), H5, APP
    openid: Optional[str] = None,
    notify_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Creates a WeChat Pay payment request.
    
    Args:
        amount: Payment amount
        currency: Payment currency (default: CNY)
        description: Payment description
        trade_type: Payment trade type
        openid: WeChat user OpenID (required for JSAPI)
        notify_url: URL for receiving payment notifications
    
    Returns:
        Dict containing payment details or error message
    """
    # Validate inputs
    if amount_error := validate_amount(amount):
        return amount_error
    if currency_error := validate_currency(currency):
        return currency_error
    if not description:
        return {"error": "Description is required"}
        
    valid_trade_types = {'NATIVE', 'JSAPI', 'H5', 'APP'}
    if trade_type not in valid_trade_types:
        return {"error": f"Invalid trade type. Must be one of: {', '.join(valid_trade_types)}"}
        
    if trade_type == 'JSAPI' and not openid:
        return {"error": "OpenID is required for JSAPI trade type"}

    payment_id = generate_id("wxpay")
    
    response = {
        "payment_id": payment_id,
        "created_at": get_current_timestamp(),
        "amount": {
            "total": int(Decimal(str(amount)) * 100),  # Convert to cents
            "currency": currency
        },
        "description": description,
        "trade_type": trade_type,
        "status": "NOTPAY",
        "expire_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", 
                                   time.gmtime(time.time() + 7200))  # 2 hours expiry
    }
    
    if trade_type == 'NATIVE':
        response["code_url"] = f"https://mock-qr.wxpay.com/{payment_id}"
    elif trade_type == 'H5':
        response["h5_url"] = f"https://mock-h5.wxpay.com/{payment_id}"
    elif trade_type == 'JSAPI':
        response["prepay_id"] = generate_id("prepay")
        response["openid"] = openid
    
    if notify_url:
        response["notify_url"] = notify_url
        
    return response

def query_wechat_pay_payment(payment_id: str) -> Dict[str, Any]:
    """
    Queries the status of a WeChat Pay payment.
    
    Args:
        payment_id: The payment ID to query
    
    Returns:
        Dict containing payment status and details
    """
    if not payment_id:
        return {"error": "Payment ID is required"}
    
    status_options = ['NOTPAY', 'SUCCESS', 'REFUND', 'CLOSED', 'REVOKED', 'PAYERROR']
    status = random.choice(status_options)
    
    response = {
        "payment_id": payment_id,
        "trade_state": status,
        "query_time": get_current_timestamp()
    }
    
    if status == 'SUCCESS':
        response.update({
            "transaction_id": generate_id("transaction"),
            "pay_time": get_current_timestamp(),
            "openid": generate_id("user"),  # Simulated user OpenID
            "bank_type": random.choice(['CMB', 'ICBC', 'CCB', 'BOC', 'ABC'])
        })
    elif status == 'PAYERROR':
        response["error_code"] = random.choice([
            "SYSTEMERROR",
            "BANK_ERROR",
            "USER_CANCELED",
            "AUTH_CODE_INVALID"
        ])
        
    return response

def stripe_create_payment(
    amount: float,
    currency: str,
    payment_method_types: list = None,
    success_url: str = None,
    cancel_url: str = None,
    customer_email: str = None,
    description: str = None,
    metadata: dict = None
) -> dict:
    """
    Create a Stripe payment session with payment links and QR code.
    
    Args:
        amount: Amount in smallest currency unit (e.g., cents for USD)
        currency: 3-letter ISO currency code (e.g., USD, EUR)
        payment_method_types: List of payment methods to accept (default: ["card"])
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect after cancelled payment
        customer_email: Customer's email address
        description: Optional description for the payment
        metadata: Optional dictionary of metadata
    
    Returns:
        dict: Payment session details including payment links and QR code URL
    """
    import time
    import uuid
    from datetime import datetime
    
    # Parameter validation
    if not amount or amount <= 0:
        return {
            "error": {
                "type": "invalid_request_error",
                "message": "Amount must be greater than 0",
                "param": "amount"
            }
        }
    
    if not currency or len(currency) != 3:
        return {
            "error": {
                "type": "invalid_request_error",
                "message": "Invalid currency code. Must be 3-letter ISO code",
                "param": "currency"
            }
        }
    
    # Default payment methods if none provided
    if not payment_method_types:
        payment_method_types = ["card"]
        
    # Generate session and payment IDs
    session_id = f"cs_{uuid.uuid4().hex[:24]}"
    payment_intent_id = f"pi_{uuid.uuid4().hex[:24]}"
    
    # Generate URLs
    checkout_url = f"https://checkout.stripe.com/c/pay/{session_id}"
    qr_code_url = f"https://qr.stripe.com/{session_id}"
    
    # Success response
    response = {
        "id": session_id,
        "object": "checkout.session",
        "payment_intent": payment_intent_id,
        "amount": amount,
        "currency": currency.lower(),
        "status": "open",
        "created": int(time.time()),
        "expires_at": int(time.time()) + 1800,  # 30 minutes expiry
        "url": checkout_url,
        "payment_method_types": payment_method_types,
        "qr_code": {
            "url": qr_code_url,
            "image_url_png": f"{qr_code_url}/png",
            "image_url_svg": f"{qr_code_url}/svg"
        },
        "success_url": success_url,
        "cancel_url": cancel_url,
        "customer_email": customer_email,
        "customer_details": None,  # Will be populated after payment
        "description": description,
        "metadata": metadata or {},
        "payment_status": "unpaid",
        "livemode": False,
        "client_secret": f"{payment_intent_id}_secret_{uuid.uuid4().hex[:24]}",
    }
    
    return response