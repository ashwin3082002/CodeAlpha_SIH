from django.core.mail import EmailMultiAlternatives
from sip_db.models import institution_id, student_id
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import random
import re
from twilio.rest import Client

def send_sms(message,to):
    account_sid = 'ACCOUNT_SID'
    auth_token = 'AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+12706791996',
    body=message,
    to='+91'+str(to)
    )
    print(message.sid,to)

    return message.sid

#send bonafide
def bonafide_mail(emailto, sname, pname, dname,cname,mobile):
    try:
        send_sms(''' 
Hey Student, 
Your Bonafide Request has been Approved by the Institution, Kindly check for the same in your email.

Regards,
TEAM SIP''',str(mobile))
    except:
        pass
    subject = 'Bonafide Approved | Student Information Portal'
    html_content = render_to_string('mail/onafide.html',{'student_name':sname,'parent_name':pname,'degree_name':dname, 'college_name':cname})
    text_content = strip_tags(html_content)
    to = emailto
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
        )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


def doc_rej(emailto):
    body = '''
    Your Request for the Document has been rejected by the institution, Kindly Contact the Institution 
    administrator/HOD/Class Teacher if you think this is as mistake.

    Regards,
    Team SIP
    '''
    send_mail(
    'DOC REQUEST REJECTED | Student Information Portal',
    body,
    settings.EMAIL_HOST_USER,
    [emailto],
    fail_silently=True,
)

    
def noc_mail(emailto, sname, pname, dname,cname):
    subject = 'NOC Approved | Student Information Portal'
    html_content = render_to_string('mail/oc_mail.html',{'student_name':sname,'parent_name':pname,'degree_name':dname, 'college_name':cname})
    text_content = strip_tags(html_content)
    to = emailto
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
        )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


#api creation mail
def api_mail_creation(emailto, orgname, api_key, apiid):
    subject = 'IMP: API ACCESS | Student Information Portal'
    to = emailto
    html_content = render_to_string('mail/create_api.html',{'name':orgname,'key':api_key,'apiid': apiid})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,    
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


#api revoke mail
def api_mail_revok(emailto, apiid):
    subject = 'API ACCESS REVOKED | Student Information Portal'
    to = emailto
    html_content = render_to_string('mail/evoke_api.html',{'apiid': apiid})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,    
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


#api key generation
def api_key_gen():
    n = random.randint(40,80)
    lst=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    api_key = str()
    for i in range(n):
        api_key+=random.choice(lst)
    return api_key


def sendotp(emailto,mobile):
    otp=random.randint(111111,999999)
    try:
        send_sms('''
Hey User,  
Your OTP for Student Information Portal is '''+str(otp)+'''. Kindly do not share this with anyone.

Regards,
TEAM SIP''',str(mobile))
    except:
        pass
    subject = 'OTP | Student Information Portal'
    to = emailto
    
    html_content = render_to_string('mail/otp_mail.html',{'otp_code':otp})
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


def insti_creation(emailto,uname,psw):
    subject = 'Institute Profile Created | Student Information Portal'
    to = emailto
    html_content = render_to_string('mail/insti_creation.html',{'uname':uname,'psw':psw})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,    
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


def stu_creation(emailto,uname,psw):
    subject = 'Student Profile Created | Student Information Portal'
    to = emailto
    html_content = render_to_string('mail/student_creation.html',{'uname':uname,'psw':psw})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,    
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return True


def check_id_stud(s):
    """
    Checks if ID is valid
    
    ID format : 0000xxxxx0
    0-int
    x-alphabet(a-z, case insensitive)
    """
    if re.search(r'^\d{4}[a-z]{5}\d{1}$', s, re.IGNORECASE):
        return True
    else:
        return False

    
def parse_id_stud(s):
    """
    Parses the id and returns the year(1234) and serial(abcde) as a dict

    :param s: ID
    :type s: str
    :return: A dict of {'year': 0000 and 'serial' : 'xxxxx0'}
    :rtype: dict
    """
    if search := re.search(r'^(\d{4})([a-z]{5}\d{1})$', s, re.IGNORECASE):
        id_temp = list(search.groups())
        return {
            'year':int(id_temp[0]),
            'serial':id_temp[1].lower()    
        }
    else:
        return False

    
def check_id_insti(s):
    """
    Checks if ID is valid
    
    ID format : xxxxx
    x-alphabet(a-z, case insensitive)
    """
    if re.search(r'^[a-z]{5}$', s, re.IGNORECASE):
        return True
    else:
        return False

    
def check_email(s):
    """
    Checks if email is valid or invalid

    :param s: email
    :type s: str
    :return: True or False
    :rtype: bool
    """
    if re.search(
        r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
        s,
        re.IGNORECASE
    ):
        return True
    else:
        return False

    
def check_phn(n):
    """
    Checks if phone number is vaild
    
    ID format : 0000xxxxx0
    0-int
    x-alphabet(a-z, case insensitive)
    """
    if re.search(r'^(?:(?:\+91)|(?:0091))?\d{10}$', n):
    # if re.search(r'^(\+91)\d{10}$', n):
        return True
    else:
        return False

def parse_phn(n):
    """
    Parses the number and returns the number without country code

    :param n: phone number
    :type s: str
    :return: phone number without country code
    :rtype: int
    """
    if search := re.search(r'^(?:(?:\+91)|(?:0091))?(\d{10})$', n):
        phn = list(search.groups())
        return int(phn[0])
    else:
        return False


def check_id(id):
    if search := re.search(r'^(S{1}|I{1})([A-Z]{6,7})$', id, re.IGNORECASE):
        id = list(search.groups())
        if id[0] == 'S':
            return 's'
        elif id[0] == 'I':
            return 'i'
        return False
    else:
        return False
    
    
def stu_id_gen():
    stu_id= student_id.objects.all()
    def id_stu():
        id = 'S'
        for i in range(7):
            a = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
            id+=a
        return id
    id=id_stu()
    while True:
        if id in stu_id:
            id=id_stu()
        else:
            s = student_id(stuid = id)
            s.save()
            break
    return id


def insti_id_gen():
    insti_id= institution_id.objects.all()
    def id_stu():
        id = 'I'
        for i in range(6):
            a = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
            id+=a
        return id
    id=id_stu()
    while True:
        if id in insti_id:
            id=id_stu()
        else:
            s = institution_id(instiid = id)
            s.save()
            break
    return id
