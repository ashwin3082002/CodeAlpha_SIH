from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import re



def sendotp(emailto):
    subject = 'OTP | Student Information Portal'
    to = emailto
    otp=random.randint(111111,999999)
    html_content = render_to_string('otp_mail.html',{'otp_code':otp})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return otp

def check_id(s):
    """
    Checks if ID is valid
    
    ID format : 0000xxxxx
    0-int
    x-alphabet(a-z, case insensitive)
    """
    if re.search(r'^\d{4}[a-z]{5}$', s, re.IGNORECASE):
        return True
    else:
        return False

def parse_id(s):
    """
    Parses the id and returns the year(1234) and serial(abcde) as a dict
    :param s: ID
    :type s: str
    :return: A dict of {'year': 0000 and 'serial' : 'xxxxx'}
    :rtype: dict
    """
    if search := re.search(r'^(\d{4})([a-z]{5})$', s, re.IGNORECASE):
        id_temp = list(search.groups())
        return {
            'year':int(id_temp[0]),
            'serial':id_temp[1]    
        }
    else:
        return False