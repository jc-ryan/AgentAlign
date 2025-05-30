import time
import re
import uuid
import random
from typing import Optional, List, Dict, Any, Union


def generate_id(prefix: str = "") -> str:
    """Generates a unique message ID."""
    return f"{prefix}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def validate_email(email: str) -> bool:
    """
    Validates email address format.
    Returns True if valid, False if invalid.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_emails(emails: List[str]) -> Optional[Dict[str, str]]:
    """
    Validates a list of email addresses.
    Returns error dict if any invalid, None if all valid.
    """
    invalid_emails = [email for email in emails if not validate_email(email)]
    if invalid_emails:
        return {"error": f"Invalid email address(es): {', '.join(invalid_emails)}"}
    return None

def validate_attachment_size(attachments: List[Dict[str, Any]], max_size_mb: int) -> Optional[Dict[str, str]]:
    """
    Validates total attachment size.
    Returns error dict if too large, None if acceptable.
    """
    total_size = sum(att.get('size', 0) for att in attachments)
    if total_size > max_size_mb * 1024 * 1024:  # Convert MB to bytes
        return {"error": f"Total attachment size exceeds {max_size_mb}MB limit"}
    return None

# Gmail Functions
def send_gmail(
    sender: str,
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    is_html: bool = False,
    priority: str = "normal",
    draft: bool = False
) -> Dict[str, Any]:
    """
    Simulates sending an email via Gmail.
    
    Args:
        sender: Sender's email address (must be gmail.com)
        to: List of recipient email addresses
        subject: Email subject
        body: Email body content
        cc: List of CC recipients
        bcc: List of BCC recipients
        attachments: List of attachment objects with name, type, and size
        is_html: Whether body content is HTML
        priority: Email priority (low, normal, high)
        draft: Whether to save as draft instead of sending
    
    Returns:
        Dict containing email details or error message
    """
    # Validate sender domain
    if not sender.endswith('@gmail.com'):
        return {"error": "Sender must be a Gmail address"}

    # Validate email addresses
    all_recipients = to + (cc or []) + (bcc or [])
    if email_error := validate_emails(all_recipients):
        return email_error

    # Validate attachments
    if attachments:
        if len(attachments) > 25:  # Gmail attachment count limit
            return {"error": "Maximum 25 attachments allowed"}
        if size_error := validate_attachment_size(attachments, 25):  # 25MB Gmail limit
            return size_error

    message_id = generate_id('gmail')
    thread_id = generate_id('thread')

    response = {
        "message_id": message_id,
        "thread_id": thread_id,
        "created_at": get_current_timestamp(),
        "sender": sender,
        "to": to,
        "subject": subject,
        "status": "draft" if draft else "sent",
        "labels": ["DRAFT"] if draft else ["SENT"]
    }

    if cc:
        response["cc"] = cc
    if bcc:
        response["bcc"] = bcc
    if attachments:
        response["attachments"] = attachments
    if is_html:
        response["content_type"] = "text/html"
    if priority != "normal":
        response["priority"] = priority

    # Add Gmail-specific metadata
    response.update({
        "size_bytes": len(body) + sum(att.get('size', 0) for att in (attachments or [])),
        "snippet": body[:100] + "..." if len(body) > 100 else body,
        "history_id": generate_id("history")
    })

    return response

# Outlook Functions
def send_outlook(
    sender: str,
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    is_html: bool = False,
    importance: str = "normal",
    draft: bool = False,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates sending an email via Outlook.
    
    Args:
        sender: Sender's email address (must be outlook.com or hotmail.com)
        to: List of recipient email addresses
        subject: Email subject
        body: Email body content
        cc: List of CC recipients
        bcc: List of BCC recipients
        attachments: List of attachment objects with name, type, and size
        is_html: Whether body content is HTML
        importance: Email importance (low, normal, high)
        draft: Whether to save as draft instead of sending
        category: Email category/flag
    
    Returns:
        Dict containing email details or error message
    """
    # Validate sender domain
    if not any(sender.endswith(domain) for domain in ['@outlook.com', '@hotmail.com']):
        return {"error": "Sender must be an Outlook or Hotmail address"}

    # Validate email addresses
    all_recipients = to + (cc or []) + (bcc or [])
    if email_error := validate_emails(all_recipients):
        return email_error

    # Validate attachments
    if attachments:
        if size_error := validate_attachment_size(attachments, 20):  # 20MB Outlook limit
            return size_error

    message_id = generate_id('outlook')
    conversation_id = generate_id('conversation')

    response = {
        "message_id": message_id,
        "conversation_id": conversation_id,
        "created_at": get_current_timestamp(),
        "sender": sender,
        "to": to,
        "subject": subject,
        "status": "draft" if draft else "sent",
        "folder": "Drafts" if draft else "Sent Items"
    }

    if cc:
        response["cc"] = cc
    if bcc:
        response["bcc"] = bcc
    if attachments:
        response["attachments"] = attachments
    if is_html:
        response["body_type"] = "html"
    if importance != "normal":
        response["importance"] = importance
    if category:
        response["category"] = category

    # Add Outlook-specific metadata
    response.update({
        "size": len(body) + sum(att.get('size', 0) for att in (attachments or [])),
        "preview": body[:200] + "..." if len(body) > 200 else body,
        "internet_message_id": f"<{message_id}@outlook.com>"
    })

    return response

# Yahoo Mail Functions
def send_yahoo_mail(
    sender: str,
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    is_html: bool = False,
    priority: str = "normal",
    draft: bool = False
) -> Dict[str, Any]:
    """
    Simulates sending an email via Yahoo Mail.
    
    Args:
        sender: Sender's email address (must be yahoo.com)
        to: List of recipient email addresses
        subject: Email subject
        body: Email body content
        cc: List of CC recipients
        bcc: List of BCC recipients
        attachments: List of attachment objects with name, type, and size
        is_html: Whether body content is HTML
        priority: Email priority (low, normal, high)
        draft: Whether to save as draft instead of sending
    
    Returns:
        Dict containing email details or error message
    """
    # Validate sender domain
    if not sender.endswith('@yahoo.com'):
        return {"error": "Sender must be a Yahoo Mail address"}

    # Validate email addresses
    all_recipients = to + (cc or []) + (bcc or [])
    if email_error := validate_emails(all_recipients):
        return email_error

    # Validate attachments
    if attachments:
        if size_error := validate_attachment_size(attachments, 25):  # 25MB Yahoo limit
            return size_error

    message_id = generate_id('yahoo')

    response = {
        "message_id": message_id,
        "created_at": get_current_timestamp(),
        "sender": sender,
        "to": to,
        "subject": subject,
        "status": "draft" if draft else "sent",
        "folder": "Draft" if draft else "Sent"
    }

    if cc:
        response["cc"] = cc
    if bcc:
        response["bcc"] = bcc
    if attachments:
        response["attachments"] = attachments
    if is_html:
        response["format"] = "html"
    if priority != "normal":
        response["priority"] = priority

    # Add Yahoo-specific metadata
    response.update({
        "size": len(body) + sum(att.get('size', 0) for att in (attachments or [])),
        "raw_size": len(body),
        "preview": body[:150] + "..." if len(body) > 150 else body
    })

    return response

# 163 Mail Functions
def send_163_mail(
    sender: str,
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    is_html: bool = False,
    priority: str = "normal",
    draft: bool = False
) -> Dict[str, Any]:
    """
    Simulates sending an email via 163 Mail.
    
    Args:
        sender: Sender's email address (must be 163.com)
        to: List of recipient email addresses
        subject: Email subject
        body: Email body content
        cc: List of CC recipients
        bcc: List of BCC recipients
        attachments: List of attachment objects with name, type, and size
        is_html: Whether body content is HTML
        priority: Email priority (low, normal, high)
        draft: Whether to save as draft instead of sending
    
    Returns:
        Dict containing email details or error message
    """
    # Validate sender domain
    if not sender.endswith('@163.com'):
        return {"error": "Sender must be a 163 Mail address"}

    # Validate email addresses
    all_recipients = to + (cc or []) + (bcc or [])
    if email_error := validate_emails(all_recipients):
        return email_error

    # Validate attachments
    if attachments:
        if size_error := validate_attachment_size(attachments, 50):  # 50MB 163 limit
            return size_error

    message_id = generate_id('163')

    response = {
        "message_id": message_id,
        "created_at": get_current_timestamp(),
        "sender": sender,
        "to": to,
        "subject": subject,
        "status": "draft" if draft else "sent",
        "folder": "草稿箱" if draft else "已发送"
    }

    if cc:
        response["cc"] = cc
    if bcc:
        response["bcc"] = bcc
    if attachments:
        response["attachments"] = attachments
    if is_html:
        response["content_type"] = "html"
    if priority != "normal":
        response["priority"] = priority

    # Add 163-specific metadata
    response.update({
        "size": len(body) + sum(att.get('size', 0) for att in (attachments or [])),
        "preview": body[:100] + "..." if len(body) > 100 else body,
        "encoding": "utf-8"
    })

    return response

def send_twilio_sms(
    to: str,
    message: str,
    from_number: Optional[str] = None,
    media_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates sending SMS via Twilio
    
    Args:
        to: Recipient's phone number (E.164 format: +1234567890)
        message: The text message to send
        from_number: Sender's phone number (optional)
        media_url: URL of media to attach to message (optional)
    """
    def validate_phone(phone: str) -> bool:
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))
    
    def generate_twilio_sid() -> str:
        return f"SM{uuid.uuid4().hex[:32]}"
    
    # Validate required parameters
    if not to:
        return {
            "status": "error",
            "code": 21211,
            "message": "The 'To' number is required.",
            "more_info": "https://www.twilio.com/docs/errors/21211"
        }
    
    if not message:
        return {
            "status": "error",
            "code": 21602,
            "message": "Message body is required.",
            "more_info": "https://www.twilio.com/docs/errors/21602"
        }
    
    # Validate phone number format
    if not validate_phone(to):
        return {
            "status": "error",
            "code": 21217,
            "message": "Phone number is not in E.164 format",
            "more_info": "https://www.twilio.com/docs/errors/21217"
        }
    
    # Generate success response
    current_time = int(time.time())
    message_sid = generate_twilio_sid()
    
    return {
        "status": "queued",
        "sid": message_sid,
        "account_sid": "AC0123456789abcdef0123456789abcdef",
        "to": to,
        "from": from_number or "+12065550100",
        "body": message,
        "num_segments": str(len(message) // 160 + 1),
        "direction": "outbound-api",
        "api_version": "2010-04-01",
        "price": None,  # Price is only populated after delivery
        "date_created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
        "date_sent": None,  # Will be populated after delivery
        "error_code": None,
        "error_message": None,
        "uri": f"/2010-04-01/Accounts/AC0123456789abcdef0123456789abcdef/Messages/{message_sid}.json",
        "media_url": media_url
    }

def send_messagebird_sms(
    to: str,
    message: str,
    originator: Optional[str] = None,
    reference: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates sending SMS via MessageBird
    
    Args:
        to: Recipient's phone number (international format)
        message: The text message to send
        originator: Sender ID (phone number or alphanumeric, max 11 chars)
        reference: Custom reference for message
    """
    def validate_phone(phone: str) -> bool:
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))
    
    def validate_originator(orig: str) -> bool:
        if orig.startswith('+'):
            return validate_phone(orig)
        return len(orig) <= 11 and orig.isalnum()
    
    # Validate required parameters
    if not to:
        return {
            "status": "error",
            "code": 2,
            "description": "Request not valid",
            "errors": [{"parameter": "to", "message": "to is required"}]
        }
    
    if not message:
        return {
            "status": "error",
            "code": 2,
            "description": "Request not valid",
            "errors": [{"parameter": "message", "message": "message is required"}]
        }
    
    # Validate phone number format
    if not validate_phone(to):
        return {
            "status": "error",
            "code": 9,
            "description": "Invalid phone number format",
            "errors": [{"parameter": "to", "message": "invalid phone number"}]
        }
    
    # Validate originator if provided
    if originator and not validate_originator(originator):
        return {
            "status": "error",
            "code": 9,
            "description": "Invalid originator format",
            "errors": [{"parameter": "originator", "message": "invalid originator"}]
        }
    
    # Generate success response
    current_time = int(time.time())
    
    return {
        "id": str(uuid.uuid4()),
        "status": "sent",
        "href": f"https://rest.messagebird.com/messages/{uuid.uuid4()}",
        "direction": "mt",
        "type": "sms",
        "originator": originator or "MessageBird",
        "body": message,
        "reference": reference,
        "validity": None,
        "gateway": 240,
        "typeDetails": {},
        "datacoding": "plain",
        "mclass": 1,
        "scheduledDatetime": None,
        "createdDatetime": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.localtime(current_time)),
        "recipients": {
            "totalCount": 1,
            "totalSentCount": 1,
            "totalDeliveredCount": 0,
            "totalDeliveryFailedCount": 0,
            "items": [
                {
                    "recipient": int(to[1:]),  # Remove '+' and convert to integer
                    "status": "sent",
                    "statusDatetime": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.localtime(current_time)),
                    "recipientCountry": "country",
                    "recipientCountryPrefix": int(to[1:3]),
                    "recipientOperator": "operator",
                    "messageLength": len(message),
                    "statusReason": "none",
                    "price": {"amount": 0.05, "currency": "EUR"}
                }
            ]
        }
    }

def send_telegram_message(
    chat_id: Union[int, str],
    text: str,
    parse_mode: Optional[str] = None,
    disable_notification: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Simulates sending message via Telegram Bot API
    
    Args:
        chat_id: Unique identifier for target chat
        text: Text of the message to send
        parse_mode: Mode for parsing entities ('HTML', 'Markdown', 'MarkdownV2')
        disable_notification: Send message silently
    """
    def validate_parse_mode(mode: Optional[str]) -> bool:
        if mode is None:
            return True
        return mode in ['HTML', 'Markdown', 'MarkdownV2']
    
    # Validate required parameters
    if not chat_id:
        return {
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: chat_id is required"
        }
    
    if not text:
        return {
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: text is required"
        }
    
    # Validate parse_mode if provided
    if not validate_parse_mode(parse_mode):
        return {
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: Invalid parse_mode specified"
        }
    
    # Generate success response
    current_time = int(time.time())
    
    return {
        "ok": True,
        "result": {
            "message_id": int(time.time() * 1000) % 1000000,
            "from": {
                "id": 123456789,
                "is_bot": True,
                "first_name": "YourBot",
                "username": "your_bot"
            },
            "chat": {
                "id": str(chat_id) if isinstance(chat_id, (int, str)) else str(random.randint(100000000, 999999999)),
                "type": "private" if str(chat_id).startswith("-") else "group",
                "title": "Group" if str(chat_id).startswith("-") else None,
                "username": None
            },
            "date": current_time,
            "text": text,
            "entities": []  # Would contain message entities if parse_mode was used
        }
    }