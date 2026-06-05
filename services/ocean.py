import requests
import config
from utils.logger import logger

class OceanService:
    def __init__(self):
        self.api_key = config.OCEAN_API_KEY
        self.base_url = "https://api.ocean.io/v3"

    def get_similar_companies(self, seed_domain):
        logger.info(f"Finding companies similar to {seed_domain} via Ocean.io...")
        
        headers = {
            "X-Api-Token": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "companiesFilters": {
                "lookalikeDomains": [seed_domain]
            },
            "size": 10
        }

        try:
            response = requests.post(f"{self.base_url}/search/companies", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            companies = [c.get("company", {}).get("domain") for c in data.get("companies", []) if c.get("company", {}).get("domain")]
            logger.info(f"Found {len(companies)} similar companies.")
            return companies
        except Exception as e:
            logger.error(f"Error calling Ocean.io: {e}")
            return []
