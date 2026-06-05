import requests
import config
from utils.logger import logger
from models.contact import Contact

class ProspeoService:
    def __init__(self):
        self.api_key = config.PROSPEO_API_KEY
        self.base_url = "https://api.prospeo.io"

    def get_contacts(self, domain):
        logger.info(f"Finding decision makers for {domain} via Prospeo...")
        
        headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "page": 1,
            "filters": {
                "company": {
                    "websites": {
                        "include": [domain]
                    }
                },
                "person_seniority": {
                    "include": ["C-Suite", "Vice President", "Founder/Owner"]
                }
            }
        }

        try:
            response = requests.post(f"{self.base_url}/search-person", json=payload, headers=headers)
            if response.status_code == 400:
                data = response.json()
                if data.get("error_code") == "NO_RESULTS":
                    logger.warning(f"No results found for {domain} on Prospeo.")
                    return []
                logger.error(f"Prospeo 400 Error: {response.text}")
            response.raise_for_status()
            data = response.json()
            
            contacts = []
            for result in data.get("results", []):
                person = result.get("person", {})
                if person.get("linkedin_url"):
                    name_parts = person.get("full_name", "").split(" ", 1)
                    first_name = name_parts[0] if name_parts else "Friend"
                    last_name = name_parts[1] if len(name_parts) > 1 else ""
                    
                    contacts.append(Contact(
                        first_name=first_name,
                        last_name=last_name,
                        job_title=person.get("current_job_title"),
                        company_domain=domain,
                        linkedin_url=person.get("linkedin_url")
                    ))
            
            logger.info(f"Found {len(contacts)} contacts for {domain}.")
            return contacts
        except Exception as e:
            logger.error(f"Error calling Prospeo for {domain}: {e}")
            return []
