import sys
import json
from services.ocean import OceanService
from services.prospeo import ProspeoService
from services.eazyreach import EazyreachService
from services.brevo import BrevoService
from utils.logger import logger, console
from utils.email_templates import get_outreach_template

def run_pipeline(seed_domain):
    logger.info(f"Starting pipeline for: {seed_domain}")
    
    # 1. Ocean.io
    ocean = OceanService()
    companies = ocean.get_similar_companies(seed_domain)
    
    if not companies:
        logger.warning("No similar companies found.")
        return

    all_contacts = []
    prospeo = ProspeoService()
    eazyreach = EazyreachService()

    # 2. Prospeo & 3. Eazyreach
    for domain in companies:
        contacts = prospeo.get_contacts(domain)
        for contact in contacts:
            email = eazyreach.resolve_email(contact.linkedin_url)
            if email:
                contact.email = email
                contact.personalized_message = get_outreach_template(contact.first_name, domain)
                all_contacts.append(contact)

    # 4. Safety Checkpoint
    if not all_contacts:
        logger.warning("No contacts resolved.")
        return

    console.print(f"\n[bold green]Ready to send {len(all_contacts)} emails:[/bold green]")
    for c in all_contacts:
        console.print(f"- {c.first_name} {c.last_name} ({c.email}) at {c.company_domain}")

    confirm = console.input("\nProceed with sending? (y/n): ")
    if confirm.lower() != 'y':
        logger.info("Outreach aborted by user.")
        return

    # 5. Brevo
    brevo = BrevoService()
    for contact in all_contacts:
        brevo.send_email(
            contact.email, 
            "Thinking about your growth at " + contact.company_domain,
            contact.personalized_message,
            to_name=f"{contact.first_name} {contact.last_name}"
        )

    # Save output
    with open("output/run.json", "w") as f:
        json.dump([c.dict() for c in all_contacts], f, indent=4)
    
    logger.info("Pipeline completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]Usage: python main.py <seed_domain>[/red]")
    else:
        run_pipeline(sys.argv[1])
