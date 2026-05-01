from django.conf import settings
import logging
import re

logger = logging.getLogger(__name__)


def normalize_phone_number(phone_number, default_country_code='+254'):
    phone_number = (phone_number or '').strip().replace(' ', '').replace('-', '')
    if not phone_number:
        return ''
    if phone_number.startswith('+'):
        return phone_number
    if phone_number.startswith('0'):
        return f'{default_country_code}{phone_number[1:]}'
    return f'{default_country_code}{phone_number}'


def is_valid_phone_number(phone_number):
    return bool(re.match(r'^\+[1-9]\d{1,14}$', phone_number or ''))

def send_sms(to_phone, message, sender_name="LOcalH"):
    """
    Send SMS using Twilio if configured, otherwise log the message
    """
    try:
        # Validate phone number format
        if not is_valid_phone_number(to_phone):
            error_msg = f"Invalid phone number format: {to_phone}. Must be in E.164 format (e.g., +254XXXXXXXXX)"
            logger.error(error_msg)
            return error_msg

        # Check if Twilio is configured
        if not all([hasattr(settings, 'TWILIO_ACCOUNT_SID'), 
                   hasattr(settings, 'TWILIO_AUTH_TOKEN'), 
                   hasattr(settings, 'TWILIO_PHONE_NUMBER')]):
            error_msg = "Twilio credentials not properly configured in settings"
            logger.error(error_msg)
            return error_msg

        if not all([settings.TWILIO_ACCOUNT_SID, 
                   settings.TWILIO_AUTH_TOKEN, 
                   settings.TWILIO_PHONE_NUMBER]):
            error_msg = "Twilio credentials are empty in settings"
            logger.error(error_msg)
            return error_msg

        from twilio.rest import Client
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_number = settings.TWILIO_PHONE_NUMBER

        logger.info(f"Attempting to send SMS to {to_phone} from {twilio_number}")
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"[{sender_name}] {message}",
            from_=twilio_number,
            to=to_phone
        )
        
        logger.info(f"SMS sent successfully. Message SID: {message.sid}")
        return message.sid

    except Exception as e:
        error_msg = f"Error sending SMS: {str(e)}"
        logger.error(error_msg)
        return error_msg
