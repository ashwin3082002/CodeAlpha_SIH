from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random



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