from pydantic import BaseModel
from typing import Optional, List

class Contact(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    company_domain: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    personalized_message: Optional[str] = None
