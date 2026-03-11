import re

def validate_email(email: str):
    """
    Validate if an email address is correctly formatted.
    
    :param email: Email address to validate.
    :return: True if email is valid, None if it's invalid.
    """
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(email_regex, email):
        return True
    else:
        return None