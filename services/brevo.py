import requests
import config
from utils.logger import logger

class BrevoService:
    def __init__(self):
        self.api_key = config.BREVO_API_KEY
        self.base_url = "https://api.brevo.com/v3"

    def send_email(self, to_email, subject, body, to_name=None):
        logger.info(f"Sending email to {to_email} via Brevo...")
        
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "sender": {
                "name": config.SENDER_NAME,
                "email": config.SENDER_EMAIL
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_name or to_email
                }
            ],
            "subject": subject,
            "textContent": body
        }

        try:
            response = requests.post(f"{self.base_url}/smtp/email", json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Error calling Brevo for {to_email}: {e}")
            return False
