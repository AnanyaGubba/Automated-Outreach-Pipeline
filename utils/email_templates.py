def get_outreach_template(first_name, company_domain):
    name = first_name if first_name else "there"
    return f"""
Hi {name},

I noticed the work you're doing at {company_domain} and was really impressed.
We help companies like yours scale their outreach efforts using automation.

Would you be open to a quick 10-minute chat next week to see if we can help?

Best,
The Team
"""
