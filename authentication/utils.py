from django.conf import settings
import requests


def verify_recaptcha(g_token: str) -> bool:
    data = {
        'response': g_token,
        'secret': settings.RE_CAPTCHA_SECRET_KEY
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()
    return result_json.get('success') is True

from django.core.mail import EmailMessage

#------------------------------------------------------------------------#

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        email.send()