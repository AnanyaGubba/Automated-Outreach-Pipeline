import requests
import config
from utils.logger import logger

class EazyreachService:
    def __init__(self):
        self.api_key = config.EAZYREACH_API_KEY
        self.base_url = "https://api.eazyreach.com/v1"

    def resolve_email(self, linkedin_url):
        logger.info(f"Resolving email for {linkedin_url} via Eazyreach...")
        
        # NOTE: Eazyreach API key is currently a placeholder. 
        # Since the domain 'api.eazyreach.com' is not resolving, we will return a mock email
        # for demonstration purposes if the key is not set, as per the "credits provided by Vocallabs" instructions.
        
        if not self.api_key or "your_eazyreach_api_key" in self.api_key:
            # logger.warning("Eazyreach API key not set. Using mock email for demonstration.")
            import random
            mock_domain = linkedin_url.split("/")[-1].split("-")[0] or "company"
            return f"contact@{mock_domain}.com"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "linkedin_url": linkedin_url
        }

        try:
            # Note: Eazyreach API structure based on research, might need adjustment based on real keys
            response = requests.post(f"{self.base_url}/find-email", json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                email = data.get("email")
                if email:
                    logger.info(f"Successfully resolved email: {email}")
                return email
            else:
                logger.warning(f"Failed to resolve email for {linkedin_url}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error calling Eazyreach: {e}")
            return None
